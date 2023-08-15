import enum
import typing

import mirai


class ResponseType(enum.Enum):
    CONTENT = "content"
    """纯文本，markdown语法"""
    
    COMPONENT = "component"
    """YiriMirai的消息组件"""
    
    FUNCTION_CALL = "function_call"
    """函数调用请求（由底层处理调用过程）
    
    {
        "name": str,
        "args": dict[str, any]
    }
    """
    
    FUNCTION_RETURN = "function_return"
    """函数调用返回值
    
    {
        "name": str,
        "return": any
    }
    """


class ResponseFinishReason(enum.Enum):
    FUNCTION_CALL = "function_call"
    """由于得到函数调用请求而返回"""
    
    FUNCTION_RETURN = "function_return"
    """由于得到函数调用返回值而返回"""
    
    STOP = "stop"
    """普通内容响应结束"""
    
    LENGTH = "length"
    """普通内容响应达到长度上限而返回"""
    
    NULL = "null"
    """处于流式响应时，每一次响应的finish_reason都为null"""


class Response:
    
    role: str
    """响应的角色
    """
    
    resp_type: ResponseType
    """响应的类型"""
    
    content: typing.Union[str, dict[str, typing.Any], mirai.MessageChain]
    """响应内容(stream时为接口当前请求接收到的完整内容)"""
    
    finish_reason: ResponseFinishReason
    """此响应返回原因"""

    def set_component(self, component: mirai.MessageChain):
        """设置响应内容为组件
        """
        self.resp_type = ResponseType.COMPONENT
        self.content = component


class QueryContext:
    """一次请求的上下文
    """
    
    launcher: str
    """请求的发起者标识符
    
    这个标识符由适配器自行定义，最终用于回复给发起者
    """
    
    origin_event: mirai.Event
    """请求的原始事件
    
    在收到消息后存储
    """
    
    message_chain: mirai.MessageChain
    """请求的消息内容
    
    在收到消息后存储
    """
    
    prompt: list[dict[str, str]]
    """此次请求的prompt
    
    在访问控制器判断结束后选择并存储，消息预处理阶段处理
    """
    
    messages: list[dict[str, str]]
    """此次请求最终的messages列表
    
    在预处理完成后由QueryFactory设置，包含prompt
    """

    response: Response
    """此次请求的响应
    
    由后端设置
    """
