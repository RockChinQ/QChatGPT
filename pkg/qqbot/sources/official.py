import logging
import typing
import datetime
import asyncio
import re
import traceback
import threading

import mirai
import botpy
import botpy.message as botpy_message
import botpy.types.message as botpy_message_type

from .. import adapter as adapter_model
from .. import blob


event_handler_mapping = {
    mirai.GroupMessage: "on_at_message_create",
    mirai.FriendMessage: "on_direct_message_create",
}


cached_message_ids = {}
"""由于QQ官方的消息id是字符串，而YiriMirai的消息id是整数，所以需要一个索引来进行转换"""

id_index = 0

def save_msg_id(message_id: str) -> int:
    """保存消息id"""
    global id_index, cached_message_ids
    
    crt_index = id_index
    id_index += 1
    cached_message_ids[str(crt_index)] = message_id
    return crt_index


class OfficialMessageConverter(adapter_model.MessageConverter):
    """QQ 官方消息转换器"""
    @staticmethod
    def yiri2target(message_chain: mirai.MessageChain):
        """将 YiriMirai 的消息链转换为 QQ 官方消息"""

        msg_list = []
        if type(message_chain) is mirai.MessageChain:
            msg_list = message_chain.__root__
        elif type(message_chain) is list:
            msg_list = message_chain
        else:
            raise Exception("Unknown message type: " + str(message_chain) + str(type(message_chain)))
        
        offcial_messages: list[dict] = []
        """
        {
            "type": "text",
            "content": "Hello World!"
        }

        {
            "type": "image",
            "content": "https://example.com/example.jpg"
        }
        """

        # 遍历并转换
        for component in msg_list:
            if type(component) is mirai.Plain:
                offcial_messages.append({
                    "type": "text",
                    "content": component.text
                })
            elif type(component) is mirai.Image:
                if component.url is not None:
                    offcial_messages.append(
                        {
                            "type": "image",
                            "content": component.url
                        }
                    )
                else:
                    logging.warning("上层组件要求以非图片URL的形式发送图片消息，但 QQ 官方 API 仅支持URL形式发送，忽略此消息。")
            elif type(component) is mirai.At:
                logging.warning("上层组件要求发送 At 消息，但 QQ 官方 API 不支持此消息类型，忽略此消息。")
            elif type(component) is mirai.AtAll:
                logging.warning("上层组件要求发送 AtAll 消息，但 QQ 官方 API 不支持此消息类型，忽略此消息。")
            elif type(component) is mirai.Voice:
                logging.warning("上层组件要求发送 Voice 消息，但 QQ 官方 API 不支持此消息类型，忽略此消息。")
            elif type(component) is blob.Forward:
                # 转发消息
                yiri_forward_node_list = component.node_list

                # 遍历并转换
                for yiri_forward_node in yiri_forward_node_list:
                    try:
                        message_chain = yiri_forward_node.message_chain
                        
                        # 平铺
                        offcial_messages.extend(OfficialMessageConverter.yiri2target(message_chain))
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
            else:
                logging.warning("不受 QQ 官方 API 适配器 支持的消息类型：" + str(type(component)))

        return offcial_messages
    
    # @staticmethod
    # def target2yiri(message_list: list[dict], message_id: int = -1):
    #     """将 QQ 官方消息转换为 YiriMirai 的消息链"""
    #     yiri_msg_list = []

    #     # 添加Source组件以标记message_id等信息
    #     yiri_msg_list.append(mirai.models.message.Source(id=message_id, time=datetime.datetime.now()))
        
    #     for message in message_list:
    #         if message['type'] == 'text':
    #             yiri_msg_list += mirai.Plain(text=message['content'])
    #         elif message['type'] == 'image':
    #             yiri_msg_list += mirai.Image(url=message['content'])
    #         else:
    #             logging.warning("无法转换为 YiriMirai 消息链组件的消息类型：" + str(message['type']) + "，忽略此消息。")
        
    #     chain = mirai.MessageChain(yiri_msg_list)

    #     return chain
    
    @staticmethod
    def extract_message_chain_from_obj(message: typing.Union[botpy_message.Message, botpy_message.DirectMessage], message_id: str = None, bot_account_id: int = 0) -> mirai.MessageChain:
        yiri_msg_list = []

        # 存id

        yiri_msg_list.append(mirai.models.message.Source(id=save_msg_id(message_id), time=datetime.datetime.now()))

        yiri_msg_list.append(mirai.At(target=bot_account_id))

        for mention in message.mentions:
            if mention.bot:
                continue

            yiri_msg_list.append(mirai.At(target=mention.id))

        for attachment in message.attachments:
            if attachment.content_type == "image":
                yiri_msg_list.append(mirai.Image(url=attachment.url))
            else:
                logging.warning("不支持的附件类型：" + attachment.content_type + "，忽略此附件。")

        content = re.sub(r"<@!\d+>", "", str(message.content))
        if content.strip() != "":
            yiri_msg_list.append(mirai.Plain(text=content))

        chain = mirai.MessageChain(yiri_msg_list)

        return chain
    

class OfficialEventConverter(adapter_model.EventConverter):
    """事件转换器"""
    @staticmethod
    def yiri2target(event: typing.Type[mirai.Event]):
        if event == mirai.GroupMessage:
            return botpy_message.Message
        elif event == mirai.FriendMessage:
            return botpy_message.DirectMessage
        else:
            raise Exception("未支持转换的事件类型(YiriMirai -> Official): " + str(event))

    @staticmethod
    def target2yiri(event: typing.Union[botpy_message.Message, botpy_message.DirectMessage]) -> mirai.Event:
        import mirai.models.entities as mirai_entities
        if type(event) == botpy_message.Message:  # 频道内，转群聊事件
            permission = "MEMBER"

            if '2' in event.member.roles:
                permission = "ADMINISTRATOR"
            elif '4' in event.member.roles:
                permission = "OWNER"

            return mirai.GroupMessage(
                sender=mirai_entities.GroupMember(
                    id=event.author.id,
                    member_name=event.author.username,
                    permission=permission,
                    group=mirai_entities.Group(
                        id=event.channel_id,
                        name=event.author.username,
                        permission=mirai_entities.Permission.Member
                    ),
                    special_title='',
                    join_timestamp=int(datetime.datetime.strptime(event.member.joined_at, "%Y-%m-%dT%H:%M:%S%z").timestamp()),
                    last_speak_timestamp=datetime.datetime.now().timestamp(),
                    mute_time_remaining=0,
                ),
                message_chain=OfficialMessageConverter.extract_message_chain_from_obj(event, event.id),
                time=int(datetime.datetime.strptime(event.timestamp, "%Y-%m-%dT%H:%M:%S%z").timestamp()),
            )
        elif type(event) == botpy_message.DirectMessage:  # 私聊，转私聊事件
            return mirai.FriendMessage(
                sender=mirai_entities.Friend(
                    id=event.guild_id,
                    nickname=event.author.username,
                    remark=event.author.username,
                ),
                message_chain=OfficialMessageConverter.extract_message_chain_from_obj(event, event.id),
                time=int(datetime.datetime.strptime(event.timestamp, "%Y-%m-%dT%H:%M:%S%z").timestamp()),
            )
        else:
            raise Exception("未支持转换的事件类型(Official -> YiriMirai): " + str(type(event)))


class OfficialAdapter(adapter_model.MessageSourceAdapter):
    """QQ 官方消息适配器"""
    bot: botpy.Client = None

    bot_account_id: int = 0

    message_converter: OfficialMessageConverter = OfficialMessageConverter()
    # event_handler: adapter_model.EventHandler = adapter_model.EventHandler()

    cfg: dict = None

    cached_official_messages: dict = {}
    """缓存的 qq-botpy 框架消息对象
    
    message_id: botpy_message.Message | botpy_message.DirectMessage
    """

    def __init__(self, cfg: dict):
        """初始化适配器"""
        self.cfg = cfg

        intents = botpy.Intents(
            public_guild_messages=True,
            direct_message=True,
        )

        self.bot = botpy.Client(intents=intents)

        # TODO 获取机器人id和昵称

    def send_message(
        self,
        target_type: str,
        target_id: str,
        message: mirai.MessageChain
    ):
        pass

    def reply_message(
        self,
        message_source: mirai.MessageEvent,
        message: mirai.MessageChain,
        quote_origin: bool = False
    ):
        print("处理 reply_message")
        message_list = self.message_converter.yiri2target(message)
        print("转换完成")
        tasks = []
        try:
            if type(message_source) == mirai.GroupMessage:
                for msg in message_list:

                    args = {
                        "channel_id": str(message_source.sender.group.id),
                        "msg_id": cached_message_ids[str(message_source.message_chain.message_id)],
                    }
                    if msg['type'] == "text":
                        args['content'] = msg['content']
                    elif msg['type'] == "image":
                        args['image'] = msg['content']
                    
                    if quote_origin:
                        args['message_reference'] = botpy_message_type.Reference(message_id=cached_message_ids[str(message_source.message_chain.message_id)])

                    print(args)

                    tasks.append(self.bot.api.post_message(**args))

            elif type(message_source) == mirai.FriendMessage:
                for msg in message_list:

                    args = {
                        "guild_id": str(message_source.sender.id),
                    }

                    if msg['type'] == "text":
                        args['content'] = msg['content']
                    elif msg['type'] == "image":
                        args['image'] = msg['content']
                    
                    if quote_origin:
                        args['message_reference'] = botpy_message_type.Reference(message_id=cached_message_ids[str(message_source.message_chain.message_id)])

                    tasks.append(self.bot.api.post_dms(**args))
            print("get event loop")

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            print(loop.is_running())
            print("run")

            async def await_all(tasks):
                try:
                    for t in tasks:
                        await t
                except:
                    traceback.print_exc()

            asyncio.run_coroutine_threadsafe(asyncio.create_task(await_all(tasks)), loop)

        except Exception as e:
            traceback.print_exc()


    def is_muted(self, group_id: int) -> bool:
        return False
    
    def register_listener(
        self,
        event_type: typing.Type[mirai.Event],
        callback: typing.Callable[[mirai.Event], None]
    ):
        
        try:
            logging.debug("注册监听器: " + str(event_type) + " -> " + str(callback))

            async def wrapper(message: typing.Union[botpy_message.Message, botpy_message.DirectMessage]):
                self.cached_official_messages[str(message.id)] = message
                logging.debug("listener called: "+str(message))
                callback(OfficialEventConverter.target2yiri(message))

            setattr(self.bot, event_handler_mapping[event_type], wrapper)
        except Exception as e:
            traceback.print_exc()
            raise e

    def unregister_listener(
        self,
        event_type: typing.Type[mirai.Event],
        callback: typing.Callable[[mirai.Event], None]
    ):
        delattr(self.bot, event_handler_mapping[event_type])

    def run_sync(self):
        self.bot.run(
            **self.cfg
        )

    def kill(self) -> bool:
        return False
