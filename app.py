from typing import Annotated, Union

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from llama_parse import LlamaParse

from converters import Converter
from globals import (AZURE_AI_APIKEY, AZURE_AI_ENDPOINT,
                     AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME,
                     LLAMAINDEX_APIKEY)

app = FastAPI()
parser = LlamaParse(
            api_key=LLAMAINDEX_APIKEY,
            result_type='markdown',
            num_workers=1,  # if multiple files passed, split in `num_workers` API calls
            verbose=True,
            language="en",  # Optionally you can define a language, default=en
            show_progress=True,
            gpt4o_mode=True,
            azure_openai_api_version=AZURE_OPENAI_API_VERSION,
            azure_openai_deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
            azure_openai_key=AZURE_AI_APIKEY,
            azure_openai_endpoint=AZURE_AI_ENDPOINT,
        )

@app.post("/convert/vision")
def convert(image_base64: Union[str, None] = None):
    if not image_base64:
        return JSONResponse(content={"error": "The image is not found"}, status_code=400)
    
    result = Converter.imageToText(image_base64)
    if "error" in result:
        return JSONResponse(content=result, status_code=403)
    return JSONResponse(content=result, status_code=200)

@app.post("/convert/any")
def convert_any(file: Annotated[UploadFile, Form()]):
    if not file:
        return JSONResponse(content={"error": "The file is not found"}, status_code=400)
    result = Converter.parse_multimodal(file, parser)
    if "error" in result:
        return JSONResponse(content=result, status_code=403)
    return JSONResponse(content=result, status_code=200)