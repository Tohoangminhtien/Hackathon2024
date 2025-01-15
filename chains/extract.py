from langchain.chains.base import Chain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import base64


class LLMExtract(Chain):
    llm: ChatOpenAI
    prompt: str

    @property
    def input_keys(self):
        return ["image", "context"]

    @property
    def output_keys(self):
        return ["extracted", "context"]

    def generate(self, image_path):
        with open(image_path, "rb") as image_file:
            base64image = base64.b64encode(image_file.read()).decode('utf-8')

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": self.prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64image}"
                    }
                }
            ]
        )
        return self.llm.invoke([message]).content

    def _call(self, inputs: dict) -> dict:
        """
        """
        image = inputs['image']
        extracted = self.generate(image)
        return {"extracted": extracted, "context": inputs['context']}
