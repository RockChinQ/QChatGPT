
class MessageRejected(Exception):
    """AccessController拒绝响应时抛出
    
    此情况不同于AccessController直接返回False。
    所有的消息都会经过AccessController，若不符合响应规则，则返回False。
    但若由一个AccessController是敏感词检查，而用户的消息中包含敏感词，则应抛出此异常。
    """