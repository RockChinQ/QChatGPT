import typing

import mirai

from ....models.frontend.adapter import interface
from ....models.system import config as cfg
from ....runtime import module
from ....models.entities import query as querymodule


mirai_api_http_params = cfg.ConfigEntry(
    "MessageInterface.yaml",
    "mirai_api_http_params",
    {
        "adapter": "WebSocketAdapter",
        "host": "localhost",
        "port": 8080,
        "verifyKey": "yirimirai",
        "qq": 123456789
    },
    """# YiriMirai的配置
# 请到配置mirai的步骤中的教程查看每个字段的信息
# adapter: 选择适配器，目前支持HTTPAdapter和WebSocketAdapter
# host: 运行mirai的主机地址
# port: 运行mirai的主机端口
# verifyKey: mirai-api-http的verifyKey
# qq: 机器人的QQ号
#
# 注意: QQ机器人配置不支持热重载及热更新"""
)


@module.component(interface.MessageAdapterFactory)
class YiriMiraiAdapterFactory(interface.MessageAdapterFactory):
    
    @classmethod
    def create(cls, config: cfg.ConfigManager) -> 'YiriMiraiAdapter':
        return YiriMiraiAdapter(config)


class YiriMiraiAdapter(interface.MessageInterface):
    """YiriMirai适配器
    """
    bot: mirai.Mirai
    
    bot_account_id: int

    def __init__(self, config: cfg.ConfigManager):
        """初始化适配器
        """
        params = config.get(mirai_api_http_params)
        
        self.bot_account_id = params['qq']
        
        if params['adapter'] == 'WebSocketAdapter':
            self.bot = mirai.Mirai(
                qq=config['qq'],
                adapter=mirai.WebSocketAdapter(
                    host=params['host'],
                    port=params['port'],
                    authKey=params['verifyKey']
                )
            )
        elif params['adapter'] == 'HTTPAdapter':
            self.bot = mirai.Mirai(
                qq=config['qq'],
                adapter=mirai.HTTPAdapter(
                    host=params['host'],
                    port=params['port'],
                    authKey=params['verifyKey']
                )
            )
        else:
            raise ValueError("Unknown adapter for YiriMirai: " + params['adapter'])
        
    def get_bot_id(self) -> str:
        return str(self.bot_account_id)
    
    def parse_launcher(self, launcher: str) -> tuple[str, int]:
        lspt = launcher.split('_')
        
        return lspt[0], int(lspt[1])

    async def send_message(
        self,
        target: str,
        origin_event: mirai.Event,
        message: mirai.MessageChain
    ):
        """发送消息
        """
        ttype, tuin = self.parse_launcher(target)
        
        if ttype == 'group':
            await self.bot.send_group_message(tuin, message)
        elif ttype == 'person':
            await self.bot.send_friend_message(tuin, message)
        else:
            raise ValueError("Unknown target type: " + ttype)

    def register_listener(
        self,
        event_type: typing.Type[mirai.Event],
        callback: typing.Callable[[mirai.Event], typing.Any]
    ):
        """注册事件监听器
        """
        self.bot.on(event_type)(callback)

    def unregister_listener(
        self,
        event_type: typing.Type[mirai.Event],
        callback: typing.Callable[[mirai.Event], typing.Any]
    ):
        """注销事件监听器
        """
        import mirai.models.bus
        assert isinstance(self.bot, mirai.Mirai)
        bus = self.bot.bus
        assert isinstance(bus, mirai.models.bus.ModelEventBus)
        
        bus.unsubscribe(event_type, callback)

    async def run(self) -> typing.Generator[querymodule.QueryContext, None, None]:
        """运行适配器
        """
        return await mirai.MiraiRunner(self.bot)._run()
    
    def support_reload(self) -> bool:
        return False
    
    def __del__(self):
        pass
