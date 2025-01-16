from langchain.chains.base import Chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from utils.common import *


class LLMAnalyTrans(Chain):
    llm: ChatOpenAI
    prompt: PromptTemplate

    @property
    def input_keys(self):
        return ["context", "question", "language"]

    @property
    def output_keys(self):
        return ["answer"]

    def _call(self, inputs: dict) -> dict:
        """
        """
        context = inputs["context"]
        question = inputs["question"]
        language = inputs["language"]

        prompt_text = self.prompt.format(
            context=context, question=question, language=language)
        text = self.llm.invoke(prompt_text).content
        return {"answer": text}
