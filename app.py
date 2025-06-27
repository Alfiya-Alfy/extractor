from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from io import BytesIO
from pdfminer.high_level import extract_text

app = Flask(__name__)
CORS(app)


@app.route('/')
def extractor_page():
    return render_template('extracting_page.html')

@app.route('/alt')
def new_page():
    return render_template('alternative_page.html')

@app.route('/extract', methods=['POST'])
def extract_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files allowed'}), 400

    try:
        text = extract_text(BytesIO(file.read()))
        # pages = [page.strip() for page in text.split('\f') if page.strip()]
        raw_pages = [page.strip() for page in text.split('\f') if page.strip()]
        pages=[]
        for i, page in enumerate(raw_pages, start=1):
            pages.append({
                "page_number": i,
                "text_content": page
            })
        return jsonify({'pages': pages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


    

