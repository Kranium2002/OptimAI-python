# optimizeai/llm_wrapper.py

import os
import openai
import requests
import google.generativeai as genai
from optimizeai.config import Config

class LLMWrapper:
    """Wrapper class for different LLMs"""

    def __init__(self, config: Config):
        self.llm_name = config.llm
        self.model = config.model
        self.api_key = config.key
        self.mode = config.mode
        self.openai_client = ""
        self.setup_llm()

    def setup_llm(self):
        """Setup the LLM based on the name and mode provided in the config"""

        if self.llm_name.startswith("openai"):
            self.openai_client = openai.OpenAI(api_key=self.api_key)
            self.llm = self.openai_llm
        elif self.llm_name.startswith("huggingface"):
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = self.api_key
            self.llm = self.huggingface_llm
        elif self.llm_name.startswith("google"):
            genai.configure(api_key=self.api_key)
            self.llm = self.google_llm
        else:
            raise ValueError(f"Unsupported LLM: {self.llm_name}")

    def openai_llm(self, prompt):
        """Call the appropriate function based on the mode provided in the config"""

        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages = [{
                "role": "system",
                "content": "You are a helpful assistant."
            }, {
                "role": "user",
                "content": prompt
            }],
            max_tokens=150
        )
        return response.choices[0].message.content

    def huggingface_llm(self, prompt):
        """Call the appropriate function based on the mode provided in the config"""

        if self.mode == "online":
            return self.huggingface_online_llm(prompt)
        elif self.mode == "offline":
            return ValueError(f"Unsupported mode: {self.mode}")
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def huggingface_online_llm(self, prompt):
        """Call the Hugging Face API to get the response"""

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{self.model}",
            headers=headers,
            json={"inputs": prompt}, timeout=10
        )
        response.raise_for_status()
        return response.json()[0]["generated_text"]

    # def huggingface_offline_llm(self, prompt):
    #     """Use the Hugging Face library to get the response locally"""
    #     from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

    #     tokenizer = AutoTokenizer.from_pretrained(self.model)
    #     model = AutoModelForCausalLM.from_pretrained(self.model)
    #     generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
    #     response = generator(prompt, max_length=150)
    #     return response[0]["generated_text"]

    def google_llm(self, prompt):
        """Call the Google AI API to get the response"""

        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        return response.text

    def send_request(self, prompt):
        """Send a request to the LLM and return the response"""

        return self.llm(prompt)
