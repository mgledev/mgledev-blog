from flask import request, jsonify
from app import app, db, limiter
from app.ocr import ocr_image
from app.corrector import correct_text
from app.pdf_generator import generate_pdf
from app.models import User, Note
from langdetect import detect
import datetime

@app.route("/upload", methods=["POST"])
@limiter.limit("5 per minute")
def upload():
    file = request.files["image"]
    token = request.headers.get("Authorization")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Prosta walidacja użytkownika przez token
    user = User.verify_token(token)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if user.plan == "free" and user.monthly_notes >= 3:
        return jsonify({"error": "Monthly limit reached"}), 403

    text = ocr_image(file)
    language = detect(text)
    corrected = correct_text(text, language=language)
    pdf_path = generate_pdf(corrected, user.email)

    # Zapis notatki w bazie
    note = Note(user_id=user.id, content=corrected, created_at=datetime.datetime.utcnow())
    db.session.add(note)
    user.monthly_notes += 1
    db.session.commit()

    return jsonify({"text": corrected, "pdf": pdf_path})