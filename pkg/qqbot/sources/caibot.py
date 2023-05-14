import mirai

from ..adapter import MessageSourceAdapter, MessageConverter, EventConverter

import cai
from cai.settings.protocol import Protocols
from cai.client import Event as caiEvent

import typing

def get_protocol(protocol: str):
    """获取协议"""
    _dict = {
        "ANDROID_PAD": Protocols.Android.PAD,
        "ANDROID_PHONE": Protocols.Android.PHONE,
        "ANDROID_WATCH": Protocols.Android.WATCH,
        "IPAD": Protocols.IPAD,
        "MACOS": Protocols.MACOS,
    }

    if protocol not in _dict:
        raise ValueError(f"不支持的协议, 请检查配置文件: {protocol}")
    
    return _dict[protocol]


class CAIMessageConverter(MessageConverter):
    """CAI消息转换器"""
    @staticmethod
    def yiri2target(message_chain: mirai.MessageChain) -> list:
        pass

    @staticmethod
    def target2yiri(message_chain: typing.Any, message_id: int = -1) -> mirai.MessageChain:
        pass


class CAIEventConverter(EventConverter):
    """CAI事件转换器"""
    @staticmethod
    def yiri2target(event: typing.Type[mirai.Event]) -> list:
        pass

    @staticmethod
    def target2yiri(event: typing.Any) -> mirai.Event:
        pass


class CAIAdapter(MessageSourceAdapter):
    """CAI框架适配器"""
    client = None

    def __init__(self, cfg: dict):
        """初始化CAI框架的对象"""
        self.client = cai.Client(
            cfg["account"],
            cfg["password"],
            get_protocol(cfg["protocol"])
        )
