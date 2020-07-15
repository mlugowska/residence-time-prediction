import os


def get_files(files_path: str, ext: str):
    files = []
    for root, dirs, filenames in os.walk(files_path):
        for name in filenames:
            if name.endswith(ext):
                files.append(os.path.join(files_path, name))
    return files
