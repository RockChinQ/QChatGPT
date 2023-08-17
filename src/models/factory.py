from .system import config as cfg

class FactoryBase:
    """工厂类的基类"""
    
    @classmethod
    async def create(cls, config: cfg.ConfigManager) -> any:
        raise NotImplementedError
