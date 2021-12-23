import os
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from .kenzie.image import upload_files, zip_files

app = Flask(__name__)

allowed_extensions = os.getenv('ALLOWED_EXTENSIONS').split(',')
file_max_size = int(os.getenv('MAX_CONTENT_LENGTH'))
files_directory = os.getenv('FILES_DIRECTORY')

app.config['MAX_CONTENT_LENGTH'] = file_max_size

@app.get('/')
def testRoute():
    return 'Upload and download files FREE!!!'
    

@app.post('/upload')
def upload():
    try:
        return upload_files()

    except RequestEntityTooLarge:
        return "Can't upload files larger than 1MB", 413

@app.get('/files')
def list_files():
    all_files = os.listdir(f'./app/{files_directory}/gif') + os.listdir(f'./app/{files_directory}/jpg') + os.listdir(f'./app/{files_directory}/png')
    return jsonify(all_files), 200

@app.get('/files/<extension>')
def list_by_extension(extension):
    return jsonify(os.listdir(f'./app/{files_directory}/{extension}')), 200

@app.get('/download/<file_name>')
def download(file_name):
    try:
        return send_from_directory(
            directory=f"./{files_directory}",
            path=file_name,
            as_attachment=True
        )

    except:
        return 'File not found', 404

@app.get('/download-zip/')
def download_zip():
    query_ext = request.args.get('file_extension')
    query_compress = int(request.args.get('compression_ratio', 5))

    if query_ext:
        return zip_files(query_ext, query_compress)

    else:
        if len(os.listdir('app/kenzie/files/gif')) == 0 and len(os.listdir('app/kenzie/files/jpg')) == 0 and len(os.listdir('app/kenzie/files/png')) == 0:
            return "Nenhum arquivo encontrado", 404

        os.system(f'cd app/kenzie/files && zip -{query_compress} -r allFiles * && mv allFiles.zip /tmp')

        return send_from_directory(
            directory="/tmp",
            path='allFiles.zip',
            as_attachment=True
        )
