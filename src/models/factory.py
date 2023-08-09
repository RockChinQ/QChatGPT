from .system import config as cfg

class FactoryBase:
    """工厂类的基类"""
    
    @classmethod
    def create(cls, config: cfg.ConfigManager) -> any:
        raise NotImplementedError
