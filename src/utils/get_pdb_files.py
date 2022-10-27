import os
import pdb
from typing import List


def get_files(files_path: str, ext: str, given_dirs: List[str], ext_a='', ext_b='', type_=''):
    files = []
    for root, dirs, filenames in os.walk(files_path):
        for dir in dirs:
            if dir in given_dirs:
                for name in os.listdir(f'{files_path}/{dir}'):
                    if not ext_a and not ext_b and not type_:
                        if name.endswith(ext):
                            files.append(os.path.join(root, dir, name))
                    elif not type_ and name.endswith((ext, ext_a, ext_b)):
                        files.append(os.path.join(root, dir, name))
                    elif type_ == 'complex' and name == f'{dir}{ext}':
                        files.append(
                            os.path.join(root, dir, name) if 'protein' not in name and 'ligand' not in name else None)
    return files


def get_md_files(files_path: str, ext: str):
    files = []
    for root, dirs, filenames in os.walk(files_path):
        for name in filenames:
            if name.endswith(ext):
                files.append(os.path.join(root, name))
    return files
