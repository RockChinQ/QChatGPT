import logging
import os
import shutil
import time

import colorlog


handlers: list[logging.Handler] = []


def add_handler(handler: logging.Handler):
    """添加handler

    Args:
        handler (logging.Handler): handler
    """
    handlers.append(handler)
    
    logging.getLogger().addHandler(handler)


def remove_handler(handler: logging.Handler):
    """移除handler

    Args:
        handler (logging.Handler): handler
    """
    handlers.remove(handler)
    
    logging.getLogger().removeHandler(handler)
    

def remove_all_handlers():
    """移除所有handler
    """
    for handler in handlers:
        logging.getLogger().removeHandler(handler)
        
    handlers.clear()
    

def get_runtime_log_file() -> str:
    """为此次运行生成日志文件
    格式: qchatgpt-yyyy-MM-dd-HH-mm-ss.log
    """

    # 检查logs目录是否存在
    if not os.path.exists("logs"):
        os.mkdir("logs")

    return "logs/qchatgpt-%s.log" % time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    

def setup_logging():
    remove_all_handlers()
    
    log_colors_config = {
        'DEBUG': 'green',  # cyan white
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'cyan',
    }
    
    console_format = "%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s (%(lineno)d) - [%(levelname)s] : %(message)s"

    console_formatter = colorlog.ColoredFormatter(
        console_format,
        log_colors=log_colors_config,
    )

    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(console_formatter)
    
    file_format = "[%(asctime)s.%(msecs)03d] %(pathname)s (%(lineno)d) - [%(levelname)s] :\n%(message)s"
    file_formatter = logging.Formatter(file_format)
    
    file_handler = logging.FileHandler(get_runtime_log_file(), encoding="utf-8")
    file_handler.setFormatter(file_formatter)
    
    add_handler(console_handler)
    add_handler(file_handler)
