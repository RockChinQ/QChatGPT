from mirai import At, GroupMessage, MessageEvent, Mirai, Plain, StrangerMessage, WebSocketAdapter, FriendMessage, Image
import pkg.openai.session
from func_timeout import func_set_timeout, FunctionTimedOut

help_text = """帮助信息：
!help - 显示帮助
!reset - 重置会话
!last - 切换到上一次的对话
!next - 切换到下一次的对话
"""

inst = None

processing = []


class QQBotManager:
    timeout = 60
    retry = 3

    bot = None

    def __init__(self, mirai_http_api_config: dict, timeout: int = 60, retry: int = 3):

        self.timeout = timeout
        self.retry = retry

        bot = Mirai(
            qq=mirai_http_api_config['qq'],
            adapter=WebSocketAdapter(
                verify_key=mirai_http_api_config['verifyKey'],
                host=mirai_http_api_config['host'],
                port=mirai_http_api_config['port']
            )
        )

        @bot.on(FriendMessage)
        async def on_friend_message(event: FriendMessage):
            return await self.on_person_message(event)

        @bot.on(StrangerMessage)
        async def on_stranger_message(event: StrangerMessage):
            return await self.on_person_message(event)

        @bot.on(GroupMessage)
        async def on_group_message(event: GroupMessage):
            return await self.on_group_message(event)

        self.bot = bot

        global inst
        inst = self

    # 统一的消息处理函数
    @func_set_timeout(timeout)
    def process_message(self, launcher_type: str, launcher_id: int, text_message: str) -> str:
        reply = ''
        session_name = "{}_{}".format(launcher_type, launcher_id)

        if text_message.startswith('!') or text_message.startswith("！"):  # 指令
            cmd = text_message[1:].strip()

            if cmd == 'help':
                reply = "[bot]" + help_text
            elif cmd == 'reset':
                pkg.openai.session.get_session(session_name).reset(explicit=True)
                reply = "[bot]会话已重置"
            elif cmd == 'last':
                pass
            elif cmd == 'next':
                pass
        else:  # 消息
            session = pkg.openai.session.get_session(session_name)
            reply = "[GPT]" + session.append(text_message)

        return reply

    async def on_person_message(self, event: MessageEvent):
        if "person_{}".format(event.sender.id) in processing:
            return await self.bot.send(event, "err:正在处理中，请稍后再试")

        reply = ''

        if event.sender.id == self.bot.qq:
            pass
        else:
            if Image in event.message_chain:
                pass
            else:
                processing.append("person_{}".format(event.sender.id))

                # 超时则重试，重试超过次数则放弃
                failed = 0
                for i in range(self.retry):
                    try:
                        reply = self.process_message('person', event.sender.id, str(event.message_chain))
                        break
                    except FunctionTimedOut:
                        failed += 1
                        continue

                if failed == self.retry:
                    reply = "err:请求超时"

                processing.remove("person_{}".format(event.sender.id))

        if reply != '':
            return await self.bot.send(event, reply)

    async def on_group_message(self, event: GroupMessage):
        if "group_{}".format(event.group.id) in processing:
            return await self.bot.send(event, "err:正在处理中，请稍后再试")

        reply = ''

        if Image in event.message_chain:
            pass
        elif At(self.bot.qq) not in event.message_chain:
            pass
        else:
            event.message_chain.remove(At(self.bot.qq))

            processing.append("group_{}".format(event.sender.id))

            # 超时则重试，重试超过次数则放弃
            failed = 0
            for i in range(self.retry):
                try:
                    reply = self.process_message('group', event.group.id, str(event.message_chain).strip())
                    break
                except FunctionTimedOut:
                    failed += 1
                    continue

            if failed == self.retry:
                reply = "err:请求超时"

            processing.remove("group_{}".format(event.sender.id))

        if reply != '':
            return await self.bot.send(event, reply)


def get_inst() -> QQBotManager:
    global inst
    return inst
