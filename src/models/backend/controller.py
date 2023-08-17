import typing

from .adapter import generator

from . import balancer
from . import processor
from ..entities import query as querymodule
from ..system import config as cfg


class BackendControllerFactory:
    """后端控制器工厂
    """
    
    @classmethod
    async def create(cls, config: cfg.ConfigManager) -> 'BackendController':
        """创建后端控制器
        """
        raise NotImplementedError


class BackendController:
    """LLM接口访问控制器
    """
    
    load_balancer: balancer.LoadBalancer
    """LLM账号负载均衡器
    """
    
    content_generator: generator.ContentGenerator
    """内容生成接口适配器
    """
    
    content_processor: processor.ContentProcessor
    """内容处理器
    """
    
    def __init__(
        self,
        load_balancer: balancer.LoadBalancer,
        content_generator: generator.ContentGenerator,
        content_processor: processor.ContentProcessor
    ):
        """初始化控制器
        """
        pass
    
    async def process(self, query: querymodule.QueryContext) -> typing.Generator[querymodule.Response, None, None]:
        """处理请求
        
        使用负载均衡器选中账号，调用内容生成器流式生成内容，使用内容处理器处理生成器的响应。
        默认情况下，内容处理器会将所有chunk拼接成完整的response，此process函数直接返回内容处理器的生成器函数。
        """
        raise NotImplementedError
