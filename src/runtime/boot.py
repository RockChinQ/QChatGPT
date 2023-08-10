import logging

from . import log

def boot():
    log.setup_logging()
    log.set_level(logging.INFO)
    
    default_namespace = "default"

    