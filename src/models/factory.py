class FactoryBase:
    """工厂类的基类"""
    
    @classmethod
    def create(cls, config: dict) -> any:
        raise NotImplementedError
