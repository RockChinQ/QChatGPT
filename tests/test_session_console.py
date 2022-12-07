import config
import unittest
import pkg.openai.session
import pkg.openai.manager


class TestOpenAISession(unittest.TestCase):
    def test_session_console(self):
        interact = pkg.openai.manager.OpenAIInteract(config.openai_config['api_key'], config.completion_api_params)

        session = pkg.openai.session.Session('test')
        print(session.append('你好'))
        print("#{}#".format(session.prompt))

        print(session.append('你叫什么名字'))
        print("#{}#".format(session.prompt))
