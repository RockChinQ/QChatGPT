import typing

T = typing.TypeVar('T')

files: dict[dict] = {}
"""单个命名空间内的配置文件及其配置项列表

schema:
{
    "filename": {
        "name": ConfigEntry
    }
}
"""


class ConfigEntry(typing.Generic[T]):
    
    filename: str
    """配置项所属文件名"""
    
    name: str
    """配置项名称"""
    
    default: any
    """配置项默认值"""
    
    comment: str
    """配置项注释"""
    
    mgr: 'ConfigManager'
    
    def __init__(
        self,
        filename: str,
        name: str,
        default: T,
        comment: str,
    ):
        global files
        
        if filename not in files:
            files[filename] = []
            
        if self.name not in files[filename]:
            files[filename][self.name] = self
        
        self.filename = filename
        self.name = name
        self.default = default
        self.comment = comment


class ConfigManager:
    
    namespace: str
    """当一个程序中存在多个ConfigManager时，用于区分不同的ConfigManager"""
    
    def __init__(self, namespace: str):
        pass
    
    def exists(self, config_entry: ConfigEntry[T]) -> bool:
        raise NotImplementedError

    def get(self, config_entry: ConfigEntry[T]) -> T:
        raise NotImplementedError
    
    def set(self, config_entry: ConfigEntry[T], value: T):
        raise NotImplementedError
    
    def load(self, filename: str=None):
        """加载配置文件
        
        Args:
            filename (str, optional): 配置文件名。若为None，则加载所有配置文件。默认为None。
        """
        raise NotImplementedError
    
    def save(self, filename: str=None):
        """写入配置文件
        
        Args:
            filename (str, optional): 配置文件名。若为None，则写入所有配置文件。默认为None。
        """
        raise NotImplementedError
