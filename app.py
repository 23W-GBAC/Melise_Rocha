from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import nibabel as nib
from nibabel.processing import conform
from utils import image_processing

import tempfile

app = Flask(__name__)
home_directory = os.path.expanduser("~")

# Set the UPLOAD_FOLDER to the Downloads folder path
UPLOAD_FOLDER = os.path.join(home_directory, 'Downloads')

ALLOWED_EXTENSIONS = {'nii', 'nii.gz'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.nii.gz' in filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file and allowed_file(file.filename):
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.filename)
        file.save(temp_file_path)

        # Get the absolute path of the uploaded file
        file_path = os.path.abspath(temp_file_path)

        image_processed = image_processing(file_path)
        original_filename_without_extension = (file.filename).replace('.nii.gz', '')
        output_filename = original_filename_without_extension + '_normalized_image.nii.gz'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        nib.save(image_processed, output_path)

        return render_template('index.html', success=True, output_filename=output_filename)

    else:
        return render_template('index.html', error='File type not allowed')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

