import mirai

from src.models.entities import query as querymodule
from src.models.frontend.sender.wrapper import MessageWrapper
from src.models.system import config as cfg
from .....models.frontend.sender import wrapper
from .....models.system import config as cfg
from .....runtime import module
from .....models.entities import query as querymodule

from . import prefix  # 保证此模块在prefix之后被加载


at_sender = cfg.ConfigEntry(
    "MessageWrapper.yaml",
    "at_sender",
    False,
    """# 群内回复消息时是否at发送者"""
)

@module.component(wrapper.MessageWrapperFactory)
class AtSenderMessageWrapperFactory(wrapper.MessageWrapperFactory):
    """at发送者的消息包装器工厂"""

    @classmethod
    async def create(cls, config: cfg.ConfigManager) -> 'AtSenderMessageWrapper':
        return AtSenderMessageWrapper(config)
    

class AtSenderMessageWrapper(wrapper.MessageWrapper):
    """at发送者的消息包装器"""

    at_sender: bool = False

    def __init__(self, config: cfg.ConfigManager):
        super().__init__(config)
        self.at_sender = config.get(at_sender)
    
    def wrap(self, query: querymodule.QueryContext):
        if self.at_sender:
            # 把response改成component
            query.response.set_component(
                mirai.MessageChain([
                    mirai.At(target=query.origin_event.sender.id),
                    mirai.Plain(text=str(query.response.content))
                ])
            )