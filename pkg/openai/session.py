import time

import pkg.openai.manager
import pkg.database.manager

sessions = {}


class SessionOfflineStatus:
    ON_GOING = 'on_going'
    EXPLICITLY_CLOSED = 'explicitly_closed'


def load_sessions():
    global sessions

    db_inst = pkg.database.manager.get_inst()

    session_data = db_inst.load_valid_sessions()

    for session_name in session_data:
        temp_session = Session(session_name)
        temp_session.name = session_name
        temp_session.create_timestamp = session_data[session_name]['create_timestamp']
        temp_session.last_interact_timestamp = session_data[session_name]['last_interact_timestamp']
        temp_session.prompt = session_data[session_name]['prompt']

        sessions[session_name] = temp_session


def get_session(session_name: str):
    global sessions
    if session_name not in sessions:
        sessions[session_name] = Session(session_name)
    return sessions[session_name]


def dump_session(session_name: str):
    global sessions
    if session_name in sessions:
        assert isinstance(sessions[session_name], Session)
        sessions[session_name].persistence()
        del sessions[session_name]


# 通用的OpenAI API交互session
class Session:
    name = ''

    prompt = ''

    user_name = 'You'
    bot_name = 'Bot'

    create_timestamp = 0

    last_interact_timestamp = 0

    def __init__(self, name: str):
        self.name = name
        self.create_timestamp = int(time.time())
        self.last_interact_timestamp = int(time.time())

    # 请求回复
    # 这个函数是阻塞的
    def append(self, text: str) -> str:
        self.prompt += self.user_name + ':' + text + '\n' + self.bot_name + ':'
        self.last_interact_timestamp = int(time.time())

        # 向API请求补全
        response = pkg.openai.manager.get_inst().request_completion(self.prompt, self.user_name + ':')

        # print(response)
        # 处理回复
        res_test = response["choices"][0]["text"]
        res_ans = res_test

        # 去除开头可能的提示
        res_ans_spt = res_test.split("\n\n")
        if len(res_ans_spt) > 1:
            del (res_ans_spt[0])
            res_ans = '\n\n'.join(res_ans_spt)

        self.prompt += "{}".format(res_ans) + '\n'
        return res_ans

    def persistence(self):
        if self.prompt == '':
            return

        db_inst = pkg.database.manager.get_inst()

        name_spt = self.name.split('_')

        subject_type = name_spt[0]
        subject_number = int(name_spt[1])

        db_inst.persistence_session(subject_type, subject_number, self.create_timestamp, self.last_interact_timestamp,
                                    self.prompt)

    def reset(self, explicit: bool = False):
        if self.prompt != '':
            self.persistence()
            if explicit:
                pkg.database.manager.get_inst().explicit_close_session(self.name, self.create_timestamp)
        self.prompt = ''
        self.create_timestamp = int(time.time())
        self.last_interact_timestamp = int(time.time())

    # 切换到上一个session
    def last_session(self):
        last_one = pkg.database.manager.get_inst().last_session(self.name, self.last_interact_timestamp)
        if last_one is None:
            return None
        else:
            self.persistence()

            self.create_timestamp = last_one['create_timestamp']
            self.last_interact_timestamp = last_one['last_interact_timestamp']
            self.prompt = last_one['prompt']
            return self

    def next_session(self):
        next_one = pkg.database.manager.get_inst().next_session(self.name, self.last_interact_timestamp)
        if next_one is None:
            return None
        else:
            self.persistence()

            self.create_timestamp = next_one['create_timestamp']
            self.last_interact_timestamp = next_one['last_interact_timestamp']
            self.prompt = next_one['prompt']
            return self

    def list_history(self, capacity: int = 10, page: int = 0):
        return pkg.database.manager.get_inst().list_history(self.name, capacity, page)
