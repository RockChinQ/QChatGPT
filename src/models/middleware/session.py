"""Session管理器

可进行多线程控制等行为。

实现新的Session管理器时，请注册SessionManager的工厂类。
"""


class Session:
    
    prompt: str
    """此session的prompt key"""
    
    messages: list[dict[str, str]]
    """此session现存的消息列表"""


class SessionManagerFactory:
    """session管理器工厂
    """
    
    @classmethod
    def create_manager(cls, config: dict) -> 'SessionManager':
        """创建session管理器
        
        Args:
            config (dict): session管理器配置。
        
        Returns:
            SessionManager: session管理器实例。
        """
        raise NotImplementedError


class SessionManager:
    """session管理器
    """
    
    sessions: dict[str, Session]
    """session字典
    
    launcher的标识符 : Session
    """
    
    def __init__(self, config: dict):
        pass
    
    def get_session(self, launcher: str) -> Session:
        """获取session
        
        Args:
            launcher (str): launcher的标识符
        
        Returns:
            Session: session
        """
        raise NotImplementedError