"""内容处理器

处理内容生成器的回复，通常用于拼装各个chunk为完整response，BackendController仅具有一个内容处理器。
实现新的内容处理器时，请注册此处理器的工厂类。
"""
import typing

from ..entities import query as querymodule
from .. import factory

class ContentProcessorFactory(factory.FactoryBase):
    """内容处理器工厂
    """
    @classmethod
    def create(cls, config: dict) -> 'ContentProcessor':
        """创建内容处理器
        """
        raise NotImplementedError


class ContentProcessor:
    """内容处理器
    """
    
    def __init__(self) -> None:
        pass
    
    async def process(self, query: querymodule.QueryContext, query_generator: typing.Generator[querymodule.Response, None, None]) -> typing.Generator[querymodule.Response, None, None]:
        """处理内容
        
        传入的query中的response内容是单次接口请求的流式响应的一个chunk。
        
        Args:
            query (querymodule.QueryContext): 请求上下文
            query_generator (typing.Generator[querymodule.Response, None, None]): chunk生成器
            
        Returns:
            typing.Generator[querymodule.Response, None, None]: 完整response生成器
        """
        raise NotImplementedError
