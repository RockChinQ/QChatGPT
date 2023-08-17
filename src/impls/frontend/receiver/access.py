import re
import random

import mirai

from ....models.frontend.receiver import access
from ....models.system import config as cfg
from ....models.entities import query as querymodule
from ....common import target
from ....models import application as app
from ....runtime import module


group_respond_rules = cfg.ConfigEntry(
    "AccessControl.yaml",
    "group_respond_rules",
    {
        "default": {
            "at": True,
            "prefix": ["/ai", "!ai", "ai"],
            "regexp": [],
            "random_rate": 0.0,
        }
    },
    """# 群内响应规则
# 符合此消息的群内消息即使不包含at机器人也会响应
# 支持消息前缀匹配及正则表达式匹配
# 支持设置是否响应at消息、随机响应概率
# 注意：由消息前缀(prefix)匹配的消息中将会删除此前缀，正则表达式(regexp)匹配的消息不会删除匹配的部分
#      前缀匹配优先级高于正则表达式匹配
# 正则表达式简明教程：https://www.runoob.com/regexp/regexp-tutorial.html
# 
# 支持针对不同群设置不同的响应规则，例如：
# group_respond_rules = {
#    "default": {
#        "at": True,
#        "prefix": ["/ai", "!ai", "！ai", "ai"],
#        "regexp": [],
#        "random_rate": 0.0,
#    },
#    "12345678": {
#        "at": False,
#        "prefix": ["/ai", "!ai", "！ai", "ai"],
#        "regexp": [],
#        "random_rate": 0.0,
#    },
# }
#
# 以上设置将会在群号为12345678的群中关闭at响应
# 未单独设置的群将使用default规则"""
)


def select_rule(rules: dict, group_id: str) -> dict:
    """选择群内响应规则
    
    Args:
        rules (dict): 群内响应规则。
        group_id (str): 群号。
    
    Returns:
        dict: 群内响应规则。
    """
    if group_id in rules:
        return rules[group_id]
    else:
        return rules["default"]


@module.component(access.AccessControllerFactory)
class DefaultAccessControllerFactory(access.AccessControllerFactory):
    
    @classmethod
    async def create(cls, config: cfg.ConfigManager) -> 'DefaultAccessController':
        """创建访问控制器
        """
        return DefaultAccessController(config)


class DefaultAccessController(access.AccessController):
    """默认访问控制器
    
    此控制器仅判断群内at、前缀、关键词、随机响应功能，放行所有私聊消息。
    """
    config: cfg.ConfigManager = None
    
    def __init__(self, config: cfg.ConfigManager):
        """初始化访问控制器
        """
        self.config = config
    
    def check(self, query: querymodule.QueryContext) -> bool:
        """检查是否允许访问
        """
    
        ltype, luin = target.parse_qq_launcher(query.launcher)
        
        if ltype == "person":
            return True
        elif ltype == "group":
            params = self.config.get(group_respond_rules)
            rule = select_rule(params, str(luin))

            bot_uin = int(app.get_application(self.config.namespace).front_controller.adapter.get_bot_id())

            if rule['at'] and mirai.At(bot_uin) in query.message_chain:
                return True
            
            plain_text = str(query.message_chain).strip()
            
            for prefix in rule['prefix']:
                if plain_text.startswith(prefix):
                    query.message_chain = mirai.MessageChain([mirai.Plain(plain_text[len(prefix):])])
                    return True
                
            for regexp in rule['regexp']:
                if re.match(regexp, plain_text):
                    return True
            
            # 取个随机数判断是否小于随机响应概率
            if random.random() < rule['random_rate']:
                return True
            
            return False
