# 1. Import thư việnviện
import warnings
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from chains.extract import LLMExtract
from chains.analysis import LLMAnalysis
from chains.translate import LLMTranslate
from utils.common import *
from dotenv import load_dotenv
import os


class MultiMediaChatBot:

    def __init__(self, open_ai_key):
        # Chain 1:
        llm = ChatOpenAI(
            temperature=0, openai_api_key=open_ai_key, model='gpt-4o-mini')
        extract_prompt = load_prompt("prompt/extract.txt")
        self.chain_1 = LLMExtract(llm=llm, prompt=extract_prompt)

        # Chain 2:
        analysis_prompt_text = load_prompt("prompt/analysis.txt")
        analysis_prompt = PromptTemplate(
            input_variables=["extracted", "context"], template=analysis_prompt_text)
        self.chain_2 = LLMAnalysis(llm=llm, prompt=analysis_prompt)

        # Chain 3:
        translate_prompt_text = load_prompt("prompt/translate.txt")
        translate_prompt = PromptTemplate(
            input_variables=["sentence"], template=translate_prompt_text)
        self.chain_3 = LLMTranslate(
            llm=llm, prompt=translate_prompt, language="Korean")

    def chat(self, image, context):
        pipeline = self.chain_1 | self.chain_2 | self.chain_3
        result = pipeline.invoke({'image': image, "context": context})
        return result['answer']


# if __name__ == "__main__":
#     load_dotenv()
#     open_ai_key = os.getenv("OPEN_AI_KEY")
#     chat = MultiMediaChatBot(open_ai_key=open_ai_key)

#     print(chat.chat("assets/scar.jpg", "Tôi nên sơ cứu như thế nào"))
