import time
import datetime

from ...models.entities import query as querymodule
from ...models.system import config as cfg
from ...models.middleware import processor
from ...runtime import module


@module.component(processor.MessagePreProcessorFactory)
class PromptPreprocessorFactory(processor.MessagePreProcessorFactory):

    @classmethod
    async def create(cls, config: cfg.ConfigManager) -> 'PromptPreprocessor':
        return PromptPreprocessor(config)


class PromptPreprocessor(processor.Preprocessor):

    def __init__(self, config: cfg.ConfigManager):
        pass

    def process(self, query: querymodule.QueryContext):
        replacements = {
            # "date_now": time.strftime("%Y-%m-%d", time.localtime()),
            "date_now": time.strftime("%Y-%m-%d", time.localtime()),
        }
        for key, value in replacements.items():
            for prompt in query.prompt:
                prompt["content"] = prompt["content"].replace("${}".format(key), value)
