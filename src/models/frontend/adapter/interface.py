"""消息处理前端适配器模型

实现新的适配器时，请注册此适配器的工厂类
"""

import typing

import mirai

from ... import factory
from ...system import config as cfg


class MessageAdapterFactory(factory.FactoryBase):
    """适配器工厂类"""
    
    @classmethod
    def create(cls, config: cfg.ConfigManager) -> 'MessageInterface':
        """创建适配器
        
        Args:
            config (dict): 适配器配置。
        
        Returns:
            MessageInterface: 适配器实例。
        """
        raise NotImplementedError


class MessageInterface:
    """IM平台适配器接口"""
    
    def __init__(self, config: cfg.ConfigManager):
        pass
    
    async def send_message(
        self,
        target: str,
        origin_event: mirai.Event,
        message: mirai.MessageChain
    ):
        """发送消息
        
        Args:
            target (str): 目标标识字符串。
            origin_event (mirai.Event): 原始事件。
            message (mirai.MessageChain): 消息内容。
        """
        raise NotImplementedError
    
    def register_listener(
        self,
        event_type: typing.Type[mirai.Event],
        callback: typing.Callable[[mirai.Event], typing.Any]
    ):
        """注册事件监听器
        
        Args:
            event_type (typing.Type[mirai.Event]): 事件类型。
            callback (typing.Callable[[mirai.Event], typing.Any]): 事件回调函数。
        """
        raise NotImplementedError
    
    def unregister_listener(
        self,
        event_type: typing.Type[mirai.Event],
        callback: typing.Callable[[mirai.Event], typing.Any]
    ):
        """注销事件监听器
        
        Args:
            event_type (typing.Type[mirai.Event]): 事件类型。
            callback (typing.Callable[[mirai.Event], typing.Any]): 事件回调函数。
        """
        raise NotImplementedError
    
    async def run(self):
        """运行适配器"""
        raise NotImplementedError
    
    def support_reload(self) -> bool:
        """标记此适配器是否支持重载
        
        支持重载的适配器，在热重载时将会被调用__del__方法，适配器须保证资源释放正确。
        若适配器不支持重载，系统将不重载消息适配器模块，并在重载其他模块后重用旧的适配器。
        """
        return False
    
    def __del__(self):
        raise NotImplementedError
    