
from ....models.frontend.sender import wrapper
from ....models.system import config as cfg
from ....runtime import module
from ....models.entities import query as querymodule


prefix_string = cfg.ConfigEntry(
    "MessageWrapper.yaml",
    "prefix_string",
    "[GPT]",
    """# 回复前缀字符串"""
)

at_sender = cfg.ConfigEntry(
    "MessageWrapper.yaml",
    "at_sender",
    False,
    """# 群内回复消息时是否at发送者"""
)


@module.component(wrapper.MessageWrapperFactory)
class DefaultMessageWrapperFactory(wrapper.MessageWrapperFactory):
    """默认消息包装器工厂
    """
    
    @classmethod
    def create(cls, config: cfg.ConfigManager) -> 'DefaultMessageWrapper':
        return DefaultMessageWrapper(config)
    

class DefaultMessageWrapper(wrapper.MessageWrapper):

    def __init__(self, config: cfg.ConfigManager):
        pass
    
    def wrap(self, query: querymodule.QueryContext):
        pass
