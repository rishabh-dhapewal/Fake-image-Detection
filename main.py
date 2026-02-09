from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import random
import numpy as np

app = Flask(__name__)
CORS(app)  # Allow requests from your HTML frontend

@app.route("/")
def home():
    return jsonify({"message": "Fake Image Detector API running ✅"})

@app.route("/predict", methods=["POST"])
def predict():
    # Check if file part is present
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Read image bytes
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # ---- DEMO LOGIC (Replace this with real model later) ----
        # Use image stats to generate a fake but plausible prediction
        arr = np.array(img)
        brightness = np.mean(arr)
        variance = np.var(arr)
        size_factor = img.size[0] * img.size[1]

        # Simple pseudo logic for demo
        score = (variance / 1000 + brightness / 255) % 1.0
        confidence = round(abs(score - 0.3), 2)

        prediction = "Real" if score > 0.55 else "AI-Generated"

        # Return JSON
        return jsonify({
            "prediction": prediction,
            "confidence": confidence
        })
    except Exception as e:
        print(e)
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
