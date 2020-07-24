import os
from typing import List

from pymol import cmd

from utils.externals import COMPLEX_PATH
from utils.get_pdb_files import get_files


def protonate_hoh(files: List):
    for file in files:
        cmd.load(file)
        cmd.h_add(selection=f'{file[-12:-4]}')

        output_path = os.path.join(COMPLEX_PATH, 'crystallographic_hoh_hh')
        output_file = os.path.join(output_path, f'{file[-12:-4]}_HH.pdb')
        cmd.save(output_file, f'{file[-12:-4]}')


def replace_h_number(line: str):
    return line.replace(f'{line[14:16]}', f'{line[15]} ') if line[14:16] else line


def remove_connectivity(files: List):
    for pdb_file in files:
        infile = open(pdb_file, 'r').readlines()
        with open(pdb_file, 'w') as outfile:
            for index, line in enumerate(infile):
                if 'CONECT' not in line:
                    line = replace_h_number(line)
                    outfile.write(line)


def run():
    file_path = os.path.join(COMPLEX_PATH, 'crystallographic_hoh')
    files = get_files(file_path, 'pdb')

    protonate_hoh(files)

    file_path_hh = os.path.join(COMPLEX_PATH, 'crystallographic_hoh_hh')
    files_hh = get_files(file_path_hh, 'pdb')
    remove_connectivity(files_hh)


run()
