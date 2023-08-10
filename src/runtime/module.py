
import typing

from ..models import factory


factories: dict[type, list[typing.Type[factory.FactoryBase]]] = {}
"""保存所有工厂类"""


def component(cls: typing.Type):
    """标记一个类为组件
    
    Args:
        cls (type): factory的基类
    """
    global factorys

    def wrapper(factory: typing.Type[factory.FactoryBase]):
        if cls not in factorys:
            factorys[cls] = []

        factorys[cls].append(factory)

        return factory

    return wrapper
