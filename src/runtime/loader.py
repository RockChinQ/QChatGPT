"""提供模块加载和热重载功能

"""
import os
import sys
import importlib.util
from typing import List


def load_modules(directory: str, recursive: bool) -> List[str]:
    """
    动态加载指定目录下的所有Python模块。

    Args:
        directory (str): 需要加载模块的目录。
        recursive (bool): 是否递归加载子目录中的模块。

    Returns:
        List[str]: 返回加载的模块名称列表。

    Raises:
        ImportError: 如果模块无法被加载，会抛出ImportError异常。
    """
    loaded_modules = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]

                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                loaded_modules.append(module_name)

        if not recursive:
            break

    return loaded_modules


def unload_modules(directory: str, recursive: bool = False, ignore_errors: bool = False):
    """
    卸载指定目录下的所有Python模块。

    Args:
        directory (str): 需要卸载模块的目录。
        recursive (bool, optional): 是否递归卸载子目录中的模块。默认为False。
        ignore_errors (bool, optional): 是否忽略KeyError异常。默认为False。

    Raises:
        KeyError: 如果模块未被加载且ignore_errors为False，会抛出KeyError异常。
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                module_name = os.path.splitext(file)[0]
                try:
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                except KeyError:
                    if not ignore_errors:
                        raise

        if not recursive:
            break
