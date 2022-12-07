import time

import pkg.openai.manager


session = {}


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

        global session
        session[name] = self

    # 请求回复
    # 这个函数是阻塞的
    def append(self, text: str) -> str:
        self.prompt += self.user_name + ':' + text + '\n'+self.bot_name+':'
        self.last_interact_timestamp = int(time.time())

        # 向API请求补全
        response = pkg.openai.manager.get_inst().request_completion(self.prompt, self.user_name+':')

        # 处理回复
        res_test = response["choices"][0]["text"]
        res_ans = res_test

        # 去除开头可能的提示
        res_ans_spt = res_test.split("\n\n")
        if len(res_ans_spt) > 1:
            del (res_ans_spt[0])
            res_ans = '\n\n'.join(res_ans_spt)

        self.prompt += "\n" + self.bot_name + ":{}".format(res_ans)
        return res_ans

    def persistence(self):
        pass
