"""响应内容包装器

将从后端获取到的模型响应信息包装成发送的格式。程序会按照顺序调用所有注册的包装器，

实现新的包装器时，请注册此包装器的工厂类
"""

import typing

from ...entities import query as querymodule
from ... import factory


class MessageWrapperFactory(factory.FactoryBase):
    
    @classmethod
    def create(cls, config: dict) -> 'MessageWrapper':
        """创建包装器
        
        Args:
            config (dict): 包装器配置。
        
        Returns:
            MessageWrapper: 包装器实例。
        """
        raise NotImplementedError


class MessageWrapper:
    """将后端响应进行处理
    """
    
    def __init__(self, config: dict):
        pass
    
    def wrap(self, query: querymodule.QueryContext):
        """对后端响应进行处理
        
        处理query中的response的内容，若转换结束后，response的type为component，则跳过后续的包装器。
        这里传入的query里的响应都是此次用户请求中单次接口请求的完整响应内容。
        
        Args:
            query (querymodule.QueryContext): 请求上下文
        """
        raise NotImplementedError
