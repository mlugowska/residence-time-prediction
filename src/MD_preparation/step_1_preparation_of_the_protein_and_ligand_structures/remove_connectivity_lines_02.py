from typing import List

from src.utils import externals
from src.utils.get_pdb_files import get_files


def read_ligand_name(pdb_file: str):
    return pdb_file[-10:-7]


def remove_connect(file_name: str, file_obj: List):
    excluded = ['CONECT', ]
    with open(file_name, 'w') as outfile:
        for index, line in enumerate(file_obj):
            if not any(s in line for s in excluded):
                outfile.write(line)


def remove_connects_from_file(structure_files: List):
    for pdb_file in structure_files:
        infile = open(pdb_file, 'r').readlines()
        ligand_code = read_ligand_name(pdb_file)
        remove_connect(file_name=f'{pdb_file[:-11]}_{ligand_code}_HH_noconnect.pdb', file_obj=infile)


def run():
    ligand_structures = get_files(externals.LIGAND_PATH, '_HH.pdb')
    remove_connects_from_file(ligand_structures)


run()
