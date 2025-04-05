import os
import uuid
import subprocess
from flask import Flask, request, send_from_directory, jsonify, render_template, Response
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
import requests
import logging
import functools
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/data/uploads'
app.config['OUTPUT_FOLDER'] = '/data/output'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'nasilbirseybuboyle1331$$**'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def check_auth(username, password):
    """Check if the username and password are valid."""
    return username == app.config['BASIC_AUTH_USERNAME'] and password == app.config['BASIC_AUTH_PASSWORD']

def authenticate():
    """Send a 401 response that enables basic auth."""
    return Response(
        'Authentication required to access this resource.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    """Decorator for routes that require authentication."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
@requires_auth
def convert_pdf():
    # Check if the post request has the file part
    if 'file' not in request.files and 'url' not in request.form:
        return jsonify({'error': 'No file or URL provided'}), 400

    # Get custom name if provided
    custom_name = request.form.get('custom_name', '').strip()

    unique_id = str(uuid.uuid4())
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], unique_id)
    os.makedirs(output_dir, exist_ok=True)

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file and allowed_file(file.filename):
            # Use custom name if provided, otherwise use original filename
            if custom_name:
                original_ext = os.path.splitext(file.filename)[1]
                filename = secure_filename(custom_name + original_ext)
            else:
                filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    else:
        url = request.form['url']
        try:
            response = requests.get(url, stream=True)
            if not response.ok:
                return jsonify({'error': f'Failed to download file: {response.status_code}'}), 400

            parsed_url = urlparse(url)
            orig_filename = os.path.basename(parsed_url.path)

            if not allowed_file(orig_filename):
                return jsonify({'error': 'URL does not point to a PDF file'}), 400

            # Use custom name if provided, otherwise use original filename
            if custom_name:
                filename = secure_filename(custom_name + '.pdf')
            else:
                filename = secure_filename(orig_filename)

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            return jsonify({'error': f'Failed to download file: {str(e)}'}), 400

    try:
        # Run pdf2htmlEX to convert PDF to HTML
        cmd = [
            'pdf2htmlEX',
            '--zoom', '1.3',
            '--process-outline', '0',
            '--dest-dir', output_dir,
            filepath
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"pdf2htmlEX conversion failed: {result.stderr}")
            return jsonify({'error': 'PDF conversion failed', 'details': result.stderr}), 500

        # Get the output HTML file (should be the same name as input but with .html extension)
        html_filename = os.path.splitext(filename)[0] + '.html'

        # Generate access URL
        host = request.host_url.rstrip('/')
        result_url = f"{host}/view/{unique_id}/{html_filename}"

        return jsonify({
            'success': True,
            'message': 'PDF converted successfully',
            'url': result_url,
            'id': unique_id
        })

    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/view/<unique_id>/<filename>')
def view_file(unique_id, filename):
    """Serve the converted HTML file"""
    return send_from_directory(os.path.join(app.config['OUTPUT_FOLDER'], unique_id), filename)

@app.route('/files')
@requires_auth
def list_files():
    """List all converted files"""
    files = []
    output_dir = app.config['OUTPUT_FOLDER']

    for folder_name in os.listdir(output_dir):
        folder_path = os.path.join(output_dir, folder_name)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith('.html'):
                    files.append({
                        'id': folder_name,
                        'name': file,
                        'url': f"/view/{folder_name}/{file}"
                    })

    return jsonify({'files': files})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
