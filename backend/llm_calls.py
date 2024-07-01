import os

from groq import Groq

# client = Groq(
#     api_key="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",
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama3-8b-8192",
# )

# print(chat_completion.choices[0].message.content)
from dotenv import load_dotenv
load_dotenv()
def llm_generate(prompt,client=Groq(
    api_key=os.getenv('groq_key'),
)):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{prompt}",
        }
    ],
    model="llama3-8b-8192",
)
    return chat_completion.choices[0].message.content


