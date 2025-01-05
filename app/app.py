from flask import Flask, Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader

# Define blueprint
pdf_blueprint = Blueprint('pdf', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pdf_blueprint.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # Extract text from PDF
            reader = PdfReader(filepath)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'

            return jsonify({'text': text}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to extract text: {str(e)}'}), 500
        finally:
            # Clean up by removing the uploaded file
            os.remove(filepath)
    else:
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

# Create and configure the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register blueprint
app.register_blueprint(pdf_blueprint, url_prefix='/pdf')

if __name__ == '__main__':
    app.run(debug=True)
