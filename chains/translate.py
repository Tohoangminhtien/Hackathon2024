from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from utils.common import *


class LLMTranslate(Chain):
    llm: ChatOpenAI
    prompt: PromptTemplate
    language: str

    @property
    def input_keys(self):
        return ["predict"]

    @property
    def output_keys(self):
        return ["answer"]

    def _call(self, inputs: dict) -> dict:
        """
        """
        predict = inputs['predict']

        prompt_text = self.prompt.format(sentence=predict, language=self.language)
        text = self.llm.invoke(prompt_text).content
        return {"answer": text}
