from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils.common import *


class LLMAnalysis(Chain):
    llm: ChatOpenAI
    prompt: PromptTemplate

    @property
    def input_keys(self):
        return ["extracted", "context"]

    @property
    def output_keys(self):
        return ["predict"]

    def _call(self, inputs: dict) -> dict:
        """
        """
        extracted = inputs['extracted']
        context = inputs['context']

        prompt_text = self.prompt.format(extracted=extracted, context=context)
        text = self.llm.invoke(prompt_text).content
        return {"predict": text}
