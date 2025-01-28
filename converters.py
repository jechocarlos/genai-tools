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
    
    async def pdfToText(pdf_file):
        parser = LlamaParse(
            api_key='llx-JRsouDmhHGxg4SnaSS3eesQKYGJ5Y5rwL3Y6CecIbrhgFhtk',
            result_type='markdown',
            num_workers=4,  # if multiple files passed, split in `num_workers` API calls
            verbose=True,
            language="en",  # Optionally you can define a language, default=en
        )
        parsed_content = await parser.load_data(pdf_file.read())

        return parsed_content
    
    def parse_multimodal(file, parser):
        file_extension = file.filename.split(".")[-1]
        # write file locally
        filename = f"{md5(file.filename.encode()).hexdigest()}.{file_extension}"
        with open(filename, "wb") as fh:
            fh.write(file.file.read())

        
        content = parser.load_data(file_path=filename)
        print(content)
        return content[0].to_json()