import os
from flask import request, send_from_directory

allowed_extensions = os.getenv('ALLOWED_EXTENSIONS').split(',')
files_directory = os.getenv('FILES_DIRECTORY')

def create_files_directory():
    if files_directory not in os.listdir('app'):
        os.system(f'cd app && mkdir {files_directory} && cd {files_directory} && mkdir gif jpg png')
create_files_directory()

def save_file(file):
    file.save(f"./app/{files_directory}/{file.filename[-3:].lower()}/{file.filename}")

def equal_file(file):
    for gif_file in os.listdir(f'./app/{files_directory}/gif'):
        if file in gif_file:
            return True

    for jpg_file in os.listdir(f'./app/{files_directory}/jpg'):
        if file in jpg_file:
            return True

    for png_file in os.listdir(f'./app/{files_directory}/png'):
        if file in png_file:
            return True
    
    return False

def upload_files():
    uploaded_files_list = []
    not_uploaded_files_list = []
    already_exists_files_list = []

    for file in request.files:
        if equal_file(request.files[file].filename):
            already_exists_files_list.append(request.files[file].filename)

        elif request.files[file].filename[-3:].lower() in allowed_extensions:
            save_file(request.files[file])
            uploaded_files_list.append(request.files[file].filename)

        else:
            not_uploaded_files_list.append(request.files[file].filename)
    
    uploaded_files_str = ', '.join(uploaded_files_list)
    not_uploaded_files_str = ', '.join(not_uploaded_files_list)
    already_exists_files_str = ', '.join(already_exists_files_list)

    if len(not_uploaded_files_list) == 0 and len(uploaded_files_list) == 0 and len(already_exists_files_list) == 0:
        return 'Select files to upload', 404

    if len(not_uploaded_files_list) == 0 and len(already_exists_files_list) == 0:
        return f"{uploaded_files_str} uploaded successfully!", 201
    
    if len(uploaded_files_list) == 0 and len(already_exists_files_list) == 0:
        return f"{not_uploaded_files_str} extension not supported. Supported: gif, jpg, png", 415
    
    if len(uploaded_files_list) == 0 and len(not_uploaded_files_list) == 0:
        return f'{already_exists_files_str} already exist on repository', 409
    
    if len(uploaded_files_list) == 0:
        return f"{already_exists_files_str} already exist on repository AND {not_uploaded_files_str} extension unsupported. Supported: gif, jpg, png", 409
    
    if len(not_uploaded_files_list) == 0:
        return f"{uploaded_files_str} uploaded successfully! BUT {already_exists_files_str} already exist on repository", 206
    
    if len(already_exists_files_list) == 0:
        return f"{uploaded_files_str} uploaded successfully, BUT {not_uploaded_files_str} extension unsupported. Supported: gif, jpg, png", 206
    
    else:
        return f"{uploaded_files_str} uploaded successfully, BUT {already_exists_files_str} already exist on repository, AND {not_uploaded_files_str} extension unsupported. Supported: gif, jpg, png", 206

def zip_files(query_ext, query_compress):
    if query_ext == 'gif':
        if len(os.listdir(f'app/{files_directory}/gif')) == 0:
            return "File not found", 404
        
        os.system(f'cd app/{files_directory}/gif && zip -{query_compress} -r gifFiles * && mv gifFiles.zip /tmp')

        return send_from_directory(
        directory="/tmp",
        path='gifFiles.zip',
        as_attachment=True
        )

    if query_ext == 'jpg':
        if len(os.listdir(f'app/{files_directory}/jpg')) == 0:
            return "File not found", 404

        os.system(f'cd app/{files_directory}/jpg && zip -{query_compress} -r jpgFiles * && mv jpgFiles.zip /tmp')

        return send_from_directory(
        directory="/tmp",
        path='jpgFiles.zip',
        as_attachment=True
        )

    if query_ext == 'png':
        if len(os.listdir(f'app/{files_directory}/png')) == 0:
            return "File not found", 404

        os.system(f'cd app/{files_directory}/png && zip -{query_compress} -r pngFiles * && mv pngFiles.zip /tmp')

        return send_from_directory(
        directory="/tmp",
        path='pngFiles.zip',
        as_attachment=True
        )
    
    else:
        return 'File extension not found', 404
