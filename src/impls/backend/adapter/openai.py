"""现在已删除对过时的Completion接口的支持，仅支持ChatCompletion接口。"""
import typing

import openai

from ....models.system import config as cfg
from ....models.backend.adapter import generator
from ....runtime import module
from ....models.entities import query as querymodule


openai_configs = cfg.ConfigEntry(
    "ContentGenerator.yaml",
    "openai_configs",
    {
        "api_keys": {
            "default": "YOUR_API_KEY"
        },
        "reverse_proxy": None
    },
    """# OpenAI的配置
# api_keys: OpenAI的API密钥
#           支持设置多个密钥，例如：
#           "api_keys": {
#               "default": "sk-1234567890",
#               "test": "sk-0987654321"
#           }
#           使用时根据负载均衡策略选中一个密钥
# reverse_proxy: 反向代理地址，例如：http://api.openai.rockchin.top/v1  (必须要有/v1)"""
)

chat_completion_args = cfg.ConfigEntry(
    "ContentGenerator.yaml",
    "chat_completion_args",
    {
        "model": "gpt-3.5-turbo"
    },
    """# OpenAI ChatCompletion的参数
# model: 模型名称"""
)


class OpenAIChatCompletionContentGenerator(generator.ContentGenerator):

    config: cfg.ConfigManager

    def __init__(self, config: cfg.ConfigManager):
        self.config = config
        openai_cfg = config.get(openai_configs)
        openai.api_base = openai_cfg['reverse_proxy'] if openai_cfg['reverse_proxy'] else openai.api_base

        # api_key在请求前由负载均衡策略选中并设置

    async def _req(self, messages: list, functions: list, **kwargs) -> dict:
        """请求OpenAI ChatCompletion
        """

        kwargs = {**kwargs, **self.config.get(chat_completion_args)}

        response = await openai.ChatCompletion.acreate(
            messages=messages,
            functions=functions,
            stream=True,
            **kwargs
        )
        return response

    async def generate(self, query: querymodule.QueryContext) -> typing.Generator[querymodule.Response, None, None]:
        """支持Function Calling的ChatCompletion适配器
        """
        functions: list = []

        while True:
            content = ""
            function_call = {
                "name": "",
                "arguments": ""
            }
            response = {}
            async for response in self._req(query.messages, functions):
                choice = response['choices'][0]['delta']

                if 'content' in choice and choice['content']:
                    content += choice['content']

                    yield querymodule.Response(
                        role="assistant",
                        resp_type=querymodule.ResponseType.CONTENT,
                        content=content,
                        finish_reason=querymodule.ResponseFinishReason.NULL
                    )

                if 'function_call' in choice and choice['function_call']:
                    function_call["name"] += choice['function_call']['name']
                    function_call["arguments"] += choice['function_call']['arguments']

            # 添加这次结果到messages
            pending_message = {
                "role": "assistant",
                "content": content if content else None,
            }

            if function_call["name"]:
                pending_message["function_call"] = function_call

            query.messages.append(pending_message)

            # 如果具有content，才判断是否stop，因为具有function_call的不可能是最后一个响应
            if content:
                yield querymodule.Response(
                    role="assistant",
                    resp_type=querymodule.ResponseType.CONTENT,
                    content=content,
                    finish_reason=response['choices'][0]['finish_reason']
                )

                # 只要finish_reason是stop，不再考虑function_call，直接退出循环，停止生成
                if response['choices'][0]['finish_reason'] == 'stop':
                    break

            # 如果函数调用不为空，yield这个function_call，调用函数
            if function_call["name"]:
                yield querymodule.Response(
                    role="assistant",
                    resp_type=querymodule.ResponseType.FUNCTION_CALL,
                    content=function_call,
                    finish_reason=querymodule.ResponseFinishReason.FUNCTION_CALL
                )
                # TODO 调用函数，将结果添加到messages

            

