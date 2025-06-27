from flask import Flask, request, jsonify
from flask_cors import CORS
from pdfminer.high_level import extract_text
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Allow requests from other origins (like file:// or localhost:5500)

@app.route('/extract', methods=['POST'])
def extract_pdf_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported'}), 400

    try:
        text = extract_text(BytesIO(file.read()))
        pages = [page.strip() for page in text.split('\f') if page.strip()]
        
        
        return jsonify({'pages': pages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

