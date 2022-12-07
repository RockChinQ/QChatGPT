import openai

inst = None


class OpenAIInteract:
    api_key = ''
    api_params = {}

    def __init__(self, api_key: str, api_params: dict):
        self.api_key = api_key
        self.api_params = api_params

        openai.api_key = self.api_key

        global inst
        inst = self

    def request_completion(self, prompt, stop):
        response = openai.Completion.create(
            prompt=prompt,
            stop=stop,
            **self.api_params
        )
        return response


def get_inst() -> OpenAIInteract:
    global inst
    return inst
