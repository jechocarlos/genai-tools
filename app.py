from flask import Flask, jsonify, request

from converters import Converter

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    image_base64 = ""
    if "image_base64" in request.json:
        image_base64 = request.json["image_base64"]
    else:
        return jsonify({"error": "The image is not found"}), 400
    
    result = Converter.imageToText(image_base64)
    if "error" in result:
        return jsonify(result), 403 # issue in decoding
    return jsonify(result), 200