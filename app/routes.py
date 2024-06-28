from flask import Blueprint, request, send_file, jsonify
import subprocess
import os
import tempfile

main = Blueprint('main', __name__)

@main.route('/convert', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            input_path = os.path.join(tmpdirname, file.filename)
            output_path = input_path.replace('.docx', '.pdf')

            file.save(input_path)

            # Use LibreOffice to convert the file
            command = f'libreoffice --headless --convert-to pdf --outdir {tmpdirname} {input_path}'
            subprocess.run(command, shell=True, check=True)

            return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify(error=str(e)), 500
