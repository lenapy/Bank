import os


def handle_uploaded_file(file, image_path):
    with open(image_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return os.path.exists(image_path)
