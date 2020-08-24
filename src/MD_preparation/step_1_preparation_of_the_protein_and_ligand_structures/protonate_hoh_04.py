import os
from typing import List

from pymol import cmd

from src.utils import externals
from src.utils.get_pdb_files import get_files


def protonate_hoh(files: List):
    for file in files:
        cmd.load(file)
        cmd.h_add(selection=f'{file[-12:-4]}')
        # import pdb; pdb.set_trace()
        output_path = os.path.join(externals.COMPLEX_PATH, 'crystallographic_hoh_hh')
        output_file = os.path.join(output_path, f'{file[-12:-4]}_HH.pdb')
        cmd.save(output_file, f'{file[-12:-4]}')


def renumber_h(line: str):
    if 'HETATM' in line and line[13] == 'H':
        if int(line[14:16]) % 2 == 0:
            return line.replace(line[14:16], f'1 ')
        return line.replace(line[14:16], f'2 ')
    return line


def remove_connectivity(files: List):
    for pdb_file in files:
        infile = open(pdb_file, 'r').readlines()
        with open(pdb_file, 'w') as outfile:
            for index, line in enumerate(infile):
                if 'CONECT' not in line:
                    line = renumber_h(line)
                    outfile.write(line)


def run():
    file_path = os.path.join(externals.COMPLEX_PATH, 'crystallographic_hoh')
    files = get_files(file_path, 'pdb')

    protonate_hoh(files)

    file_path_hh = os.path.join(externals.COMPLEX_PATH, 'crystallographic_hoh_hh')
    files_hh = get_files(file_path_hh, 'pdb')
    remove_connectivity(files_hh)


run()
