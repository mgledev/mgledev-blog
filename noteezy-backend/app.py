from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import io
from noteezy_ai import clean_text, correct_text, summarize

app = Flask(__name__)
CORS(app)

@app.route("/api/process", methods=["POST"])
def process_note():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    image = Image.open(io.BytesIO(file.read()))
    ocr_text = pytesseract.image_to_string(image, config='--oem 1 --psm 6')
    
    cleaned = clean_text(ocr_text)
    corrected = correct_text(cleaned)
    summary = summarize(corrected)

    return jsonify({
        "ocr_raw": ocr_text,
        "corrected_text": corrected,
        "summary": summary
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
