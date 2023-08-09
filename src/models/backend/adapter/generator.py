"""内容生成器

用于对接LLM接口，实现新的内容生成器时，请注册生成器工厂类。
"""

import typing

from ...entities import query as querymodule


class ContentGeneratorFactory:
    """内容生成器工厂
    """
    
    @classmethod
    def create_generator(cls, config: dict) -> 'ContentGenerator':
        """创建内容生成器
        """
        raise NotImplementedError


class ContentGenerator:
    """内容生成器
    """

    def __init__(self, config: dict):
        """初始化内容生成器
        """
        pass
    
    async def generate(self, query: querymodule.QueryContext) -> typing.Generator[querymodule.Response, None, None]:
        """生成内容
        
        这是一个生成器函数。返回的Response的content必须是此次请求生成的完整内容。
        """
        raise NotImplementedError
