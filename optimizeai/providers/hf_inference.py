from dsp import LM


class CustomLMClient(LM):
    def __init__(self):
        self.provider = "default"

        self.history = []

    def basic_request(self, prompt, **kwargs):
        pass

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        pass