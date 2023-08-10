
from src.models.system.config import ConfigEntry
from ...models.system import config as cfg
from ...runtime import module


class DefaultConfigManager(cfg.ConfigManager):
    """默认配置管理器
    """
    
    files: dict[str, dict]
    """所有配置项
    
    文件名:配置项dict
    """
    
    def __init__(self, namespace: str):
        self.namespace = namespace
        
        self.files = {}
