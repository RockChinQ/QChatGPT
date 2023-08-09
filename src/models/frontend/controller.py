"""前端控制器实现

实现前端从接收消息，处理消息，获取响应，处理回复的所有流程控制
"""

from .adapter import interface
from .receiver import access
from .sender import wrapper

from ..middleware import session
from ..middleware import prompt
from ..middleware import processor
from .. import factory
from ..system import config as cfg


class FrontControllerFactory(factory.FactoryBase):
    """前端控制器工厂类
    """
    
    @classmethod
    def create(cls, config: cfg.ConfigManager) -> 'FrontController':
        """创建前端控制器
        
        Args:
            config (dict): 配置文件
        
        Returns:
            FrontController: 前端控制器
        """
        raise NotImplementedError


class FrontController:
    
    adapter: interface.MessageInterface
    """IM消息平台适配器
    """
    
    access_controllers: list[access.AccessController]
    """访问控制器
    
    调用时，当所有的访问控制器都返回True时，才允许进入之后的步骤。
    """
    
    session_manager: session.SessionManager
    """Session管理器"""
    
    prompt_manager: prompt.PromptManager
    """prompt管理器"""
    
    preprocessors: list[processor.MessagePreProcessor]
    """消息预处理器"""
    
    message_wrappers: list[wrapper.MessageWrapper]
    """响应消息包装器
    
    调用时，将会按照列表顺序，对响应消息进行包装。
    """
    
    def __init__(
        self,
        adapter: interface.MessageInterface,
        access_controllers: list[access.AccessController],
        message_wrappers: list[wrapper.MessageWrapper],
        session_manager: session.SessionManager,
        prompt_manager: prompt.PromptManager,
        preprocessors: list[processor.MessagePreProcessor],
        config: cfg.ConfigManager
    ):
        """初始化控制器
        
        需要在此注册事件监听器。
        """
        raise NotImplementedError
    
    async def run(self):
        """运行控制器
        
        通常此方法将直接启动adapter。
        """
        raise NotImplementedError
    
    def __del__(self):
        """此方法在热重载时被调用"""
        raise NotImplementedError