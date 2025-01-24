from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from converters import Converter

app = FastAPI()

@app.post("/convert")
def convert(image_base64: Union[str, None] = None):
    if not image_base64:
        return JSONResponse(content={"error": "The image is not found"}, status_code=400)
    
    result = Converter.imageToText(image_base64)
    if "error" in result:
        return JSONResponse(content=result, status_code=403)
    return JSONResponse(content=result, status_code=200)