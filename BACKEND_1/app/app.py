@app.route('/')
def home():
    return render_template('index.html')

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def ocr():
    data = request.get_json()
    image_url = data.get("image_url", "")
    return jsonify({
        "message": "OCR route working!",
        "received_image_url": image_url
    })

if __name__ == "__main__":
    app.run(debug=True)
from flask import render_template

@app.route('/')
def home():
    return render_template('index.html')
