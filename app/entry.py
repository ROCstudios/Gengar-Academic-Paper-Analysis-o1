from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from app.analysis.gpt_analysis import get_collective_scores, get_pdf_analysis, get_analysis_by_id
#eg6b57b9uRmTGTqiij0

# Define blueprint
pdf_blueprint = Blueprint('pdf', __name__)
analysis_blueprint = Blueprint('analysis', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@analysis_blueprint.route('/all_scores', methods=['GET'])
def get_bulk_analysis():
    return jsonify(get_collective_scores())

@pdf_blueprint.route('/get_analysis/<id>', methods=['GET'])
def fetch_analysis_by_id(id):
    return jsonify(get_analysis_by_id(id))

@pdf_blueprint.route('/upload', methods=['POST'])
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
            analysis = get_pdf_analysis(filepath)
            return jsonify(analysis), 200
        except Exception as e:
            return jsonify({'error': f'Failed to extract text: {str(e)}'}), 500
        finally:
            # Clean up by removing the uploaded file
            os.remove(filepath)
    else:
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400


# Create and configure the Flask app
app = Flask(__name__)
# Enable CORS for all domains and methods
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        "supports_credentials": True
    }
})

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register blueprint
app.register_blueprint(pdf_blueprint, url_prefix='/pdf')
app.register_blueprint(analysis_blueprint, url_prefix='/analysis')

if __name__ == '__main__':
    app.run(debug=True)
