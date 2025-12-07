#导入DeepSeek v3.2 API
import os
from openai import OpenAI
class ds:

    def __init__(self):
        self.client = OpenAI(
            api_key='sk-ab45db1d205a46dbadc64106b970efa5',
            base_url="https://api.deepseek.com")

    def deepseekchat(self,q):
        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": q},
            ],
            stream=False
        )
        print('回答：' + response.choices[0].message.content)










