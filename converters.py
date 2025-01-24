import base64
import json
from hashlib import md5

import ollama
from pydantic import BaseModel


# use below to control the response of the model to be in a specific format and semantic
class VisionResponse(BaseModel):
    words_that_can_be_seen_in_image: list[str]
    understanding_of_contents: str
    image_contents: str
    description_of_contents: str
    tags: list[str]

class Converter:
    def __init__(self):
        return self
    
    def imageToText(image_base64):
        filename = f"{md5(image_base64.encode()).hexdigest()}.jpg"

        try:
            with open(filename, "wb") as fh:
                fh.write(base64.b64decode(image_base64))
        except Exception as e:
            return {"error": str(e), "message": "Error in decoding the image"}

        llm_response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': '',
                'images': [filename]
            }],
            format=VisionResponse.model_json_schema(),
            options={"temperature":0.1}
        )

        clean_response = VisionResponse.model_validate_json(llm_response.message.content).json().replace('\"', '"')
        return json.loads(clean_response)