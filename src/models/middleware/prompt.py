"""Prompt管理器

运行时仅存在一个PromptManager实例，用于管理prompt的获取和设置

实现新的PromptManager时，请注册此PromptManager的工厂类
"""

from .. import factory
from ..system import config as cfg


class PromptManagerFactory(factory.FactoryBase):
    """prompt管理器工厂
    """
    
    @classmethod
    def create(cls, config: cfg.ConfigManager) -> 'PromptManager':
        """创建prompt管理器
        
        Args:
            config (dict): prompt管理器配置
            
        Returns:
            PromptManager: prompt管理器实例
        """
        raise NotImplementedError
    

class PromptManager:
    """prompt管理器
    """
    
    def __init__(self, config: cfg.ConfigManager):
        """初始化
        """
        pass
    
    def get_prompt(self, prompt_key: str=None) -> tuple[str, list[dict[str, str]]]:
        """获取prompt
        
        Args:
            prompt_key (str): prompt的key前缀
            
        Returns:
            tuple[str, list[dict[str, str]]]: prompt的key和内容
            
        Raises:
            KeyError: 未找到对应的prompt

        """
        raise NotImplementedError

    def set_as_default(self, prompt_key: str):
        """设置默认prompt
        
        Args:
            prompt_key (str): prompt的key前缀
        """
        raise NotImplementedError