# 定义不同接口请求的模型
import threading
import asyncio

import openai


class RequestBase:

    req_func: callable

    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def _req(self, **kwargs):
        """处理代理问题"""

        ret: dict = {}

        async def awrapper(**kwargs):
            nonlocal ret

            ret = await self.req_func(**kwargs)
            return ret
            
        loop = asyncio.new_event_loop()

        thr = threading.Thread(
            target=loop.run_until_complete,
            args=(awrapper(**kwargs),)
        )

        thr.start()
        thr.join()

        return ret

    def __iter__(self):
        raise self

    def __next__(self):
        raise NotImplementedError