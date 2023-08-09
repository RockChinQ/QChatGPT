from .. import factory


class LoadBalancerFactory(factory.FactoryBase):
    """负载均衡器工厂
    """
    
    @classmethod
    def create(cls, config: dict) -> 'LoadBalancer':
        """创建负载均衡器
        """
        raise NotImplementedError


class LoadBalancer:
    """后端账号负载均衡器
    """
    
    def __init__(self, config: dict):
        """初始化负载均衡器
        """
        pass
    
    def next_account(self) -> str:
        """切换并获取下一个账号
        """
        raise NotImplementedError
    
    def get_current_account(self) -> str:
        """获取当前账号
        """
        raise NotImplementedError
