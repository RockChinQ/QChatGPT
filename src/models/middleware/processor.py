"""消息预处理器

收到新消息后，按顺序挨个调用所有预处理器。

实现新的预处理器时，请注册此预处理器的工厂类
"""

from ..entities import query as querymodule


class MessagePreProcessorFactory:
    """消息预处理器工厂
    """
    
    @classmethod
    def create_processor(cls, config: dict) -> 'MessagePreProcessor':
        """创建消息预处理器
        """
        raise NotImplementedError


class MessagePreProcessor:
    """对接收到的消息和prompt进行预处理
    """
    
    def __init__(self, config: dict):
        pass
    
    def process(self, query: querymodule.QueryContext):
        """对消息或prompt进行预处理
        """
        raise NotImplementedError
