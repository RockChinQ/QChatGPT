import mirai

class ForwardMessageDiaplay(mirai.MiraiBaseModel):
    title: str = "群聊的聊天记录"
    brief: str = "[聊天记录]"
    source: str = "聊天记录"
    preview: list[str] = []
    summary: str = "查看x条转发消息"


class Forward(mirai.MessageComponent):
    """合并转发。"""
    type: str = "Forward"
    """消息组件类型。"""
    display: ForwardMessageDiaplay
    """显示信息"""
    node_list: list[mirai.ForwardMessageNode]
    """转发消息节点列表。"""
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.node_list = args[0]
            super().__init__(**kwargs)
        super().__init__(*args, **kwargs)

    def __str__(self):
        return '[聊天记录]'
