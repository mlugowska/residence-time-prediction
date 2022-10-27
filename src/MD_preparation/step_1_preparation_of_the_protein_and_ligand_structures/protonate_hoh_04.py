from typing import List

from pymol import cmd

from src.MD_preparation.step_1_preparation_of_the_protein_and_ligand_structures.remove_connectivity_lines_02 import \
    remove_connect
from src.utils import externals
from src.utils.get_pdb_files import get_files


def protonate_hoh(files: List):
    for file in files:
        cmd.load(file)
        selection = f'{file[-12:-4]}'
        cmd.h_add(selection=selection)
        cmd.save(f'{file[:-4]}_HH.pdb', selection)


def renumber_h(line: str):
    if 'HETATM' in line and line[13] == 'H':
        if int(line[14:16]) % 2 == 0:
            return line.replace(line[14:16], f'1 ')
        return line.replace(line[14:16], f'2 ')
    return line


def change_h_numbering(file_name: str, file_obj: List):
    with open(file_name, 'w') as outfile:
        for index, line in enumerate(file_obj):
            line = renumber_h(line)
            outfile.write(line)


def remove_connectivity(files: List):
    for pdb_file in files:
        infile = open(pdb_file, 'r').readlines()
        remove_connect(file_name=pdb_file, file_obj=infile)

        infile = open(pdb_file, 'r').readlines()
        change_h_numbering(file_name=pdb_file, file_obj=infile)


def run():
    pdbs = list(externals.PDB_TO_DO.keys())
    files = get_files(externals.DATA_PATH, ext='_HOH.pdb', given_dirs=pdbs, type_='complex')
    protonate_hoh(files)

    files_hh = get_files(externals.DATA_PATH, ext='_HOH_HH.pdb', given_dirs=pdbs, type_='complex')
    remove_connectivity(files_hh)


run()
