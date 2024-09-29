from __future__ import annotations

import typing
import asyncio

from ...lib import itchat

from .. import adapter
from ...core import app
from ..types import message as platform_message
from ..types import events as platform_events
from ..types import entities as platform_entities


@adapter.adapter_class("itchat")
class ItchatAdapter(adapter.MessageSourceAdapter):
    
    bot: itchat.Core

    def __init__(self, config: dict, ap: app.Application):
        self.config = config
        self.ap = ap

        self.bot = itchat.load_async_itchat()

    async def send_message(
        self, target_type: str, target_id: str, message: platform_message.MessageChain
    ):
        pass

    async def reply_message(  
        self,
        message_source: platform_events.MessageEvent,
        message: platform_message.MessageChain,
        quote_origin: bool = False,
    ):
        pass

    async def is_muted(self, group_id: int) -> bool:
        return False

    def register_listener(
        self,
        event_type: typing.Type[platform_events.Event],
        callback: typing.Callable[[platform_events.Event, adapter.MessageSourceAdapter], None],
    ):
        pass

    def unregister_listener(
        self,
        event_type: typing.Type[platform_events.Event],
        callback: typing.Callable[[platform_events.Event, adapter.MessageSourceAdapter], None],
    ):
        pass

    async def run_async(self):
        await self.bot.auto_login()
        await self.bot.run()

    async def kill(self) -> bool:
        return False
    
