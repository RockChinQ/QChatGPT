"""消息放行控制器

前端收到消息后，包装QueryContext，按照顺序调用访问控制器的judge_access方法，判断是否放行。  
任一访问控制器返回False，则不再继续调用后续访问控制器，直接丢弃此消息。  

实现新的访问控制器时，请注册此控制器的工厂类。
"""

from ...entities import query as querymodule
from ... import factory
from ...system import config as cfg


class AccessControllerFactory(factory.FactoryBase):
    """访问控制器工厂
    """
    @classmethod
    def create(cls, config: cfg.ConfigManager) -> 'AccessController':
        """创建访问控制器
        
        Args:
            config (dict): 访问控制器配置。
        
        Returns:
            AccessController: 访问控制器实例。
        """
        raise NotImplementedError


class AccessController:
    """访问控制器
    """
    
    def __init__(self, config: cfg.ConfigManager):
        pass
    
    def judge_access(self, query: querymodule.QueryContext) -> bool:
        raise NotImplementedError
