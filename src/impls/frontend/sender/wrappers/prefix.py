"""为消息纯文本添加预定前缀的消息包装器"""

from .....models.frontend.sender import wrapper
from .....models.system import config as cfg
from .....runtime import module
from .....models.entities import query as querymodule


prefix_string = cfg.ConfigEntry(
    "MessageWrapper.yaml",
    "prefix_string",
    "[GPT]",
    """# 回复前缀字符串"""
)

@module.component(wrapper.MessageWrapperFactory)
class PrefixMessageWrapperFactory(wrapper.MessageWrapperFactory):
    """加前缀包装器工厂
    """
    
    @classmethod
    async def create(cls, config: cfg.ConfigManager) -> 'PrefixMessageWrapper':
        return PrefixMessageWrapper(config)
    

class PrefixMessageWrapper(wrapper.MessageWrapper):

    config: cfg.ConfigManager

    def __init__(self, config: cfg.ConfigManager):
        self.config = config
    
    def wrap(self, query: querymodule.QueryContext):
        if query.response.resp_type == querymodule.ResponseType.CONTENT:
            query.response.content = self.config.get(prefix_string) + query.response.content
