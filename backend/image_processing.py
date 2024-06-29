import base64
from langchain_community.llms.ollama import Ollama
from langchain.schema.messages import HumanMessage, SystemMessage
from base64 import b64decode
import partition
import os
from PIL import Image
import cfg

def encode_image(image_path):
    ''' Getting the base64 string '''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def image_captioning(img_base64,prompt):
    ''' Image summary '''
    chat = Ollama(model='llava')

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text":prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        },
                    },
                ]
            )
        ]
    )
    return msg

def image_capt_summary_list(path):

    img_base64_list = []
    image_summaries = []

    prompt = "Describe the image in detail. Be specific about graphs, such as bar,line,pie plots."

    for img_file in sorted(os.listdir(path)):
        if img_file.endswith('.jpg'):
            img_path = os.path.join(path, img_file)
            base64_image = encode_image(img_path)
            img_base64_list.append(base64_image)
            img_capt = image_captioning(base64_image,prompt)
            
            image_summaries.append(img_capt) 
    return img_base64_list,image_summaries




def split_image_text_types(docs):
    ''' Split base64-encoded images and texts '''
    b64 = []
    text = []
    for doc in docs:
        try:
            b64decode(doc)
            b64.append(doc)
        except Exception as e:
            text.append(doc)
    return {
        "images": b64,
        "texts": text
    }
