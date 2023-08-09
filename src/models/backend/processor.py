"""内容处理器

处理内容生成器的回复，控制器按照顺序逐个调用内容处理器处理内容。
实现新的内容处理器时，请注册此处理器的工厂类。
"""

from ..entities import query as querymodule


class ContentProcessorFactory:
    """内容处理器工厂
    """
    @classmethod
    def create_processor(cls, config: dict) -> 'ContentProcessor':
        """创建内容处理器
        """
        raise NotImplementedError


class ContentProcessor:
    """内容处理器
    """
    
    def __init__(self) -> None:
        pass
    
    def process(self, query: querymodule.QueryContext):
        """处理内容
        
        传入的query中的response内容是单次接口请求的流式响应的一个chunk。
        """
        raise NotImplementedError
