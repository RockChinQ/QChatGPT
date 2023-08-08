"""前端控制器实现

实现前端从接收消息，处理消息，获取响应，处理回复的所有流程控制
"""

from .adapter import interface
from .receiver import access
from .sender import wrapper

from ..middleware import session
from ..middleware import prompt
from ..middleware import processor


class FrontController:
    
    adapter: interface.MessageInterface
    
    access_controllers: list[access.AccessController]
    
    message_wrappers: list[wrapper.MessageWrapper]
    
    session_manager: session.SessionManager
    
    prompt_manager: prompt.PromptManager
    
    preprocessors: list[processor.MessagePreProcessor]
    
    def __init__(
        self,
        adapter: interface.MessageInterface,
        access_controllers: list[access.AccessController],
        message_wrappers: list[wrapper.MessageWrapper],
        session_manager: session.SessionManager,
        prompt_manager: prompt.PromptManager,
        preprocessors: list[processor.MessagePreProcessor],
        config: dict
    ):
        """初始化控制器
        
        需要在此注册事件监听器。
        """
    
    def run(self):
        """运行控制器
        
        通常此方法将直接启动adapter。
        """
        raise NotImplementedError
    
    def __del__(self):
        """此方法在热重载时被调用"""
        raise NotImplementedError