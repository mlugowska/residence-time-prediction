from typing import List

from src.utils import externals
from src.utils.get_pdb_files import get_files


def remove_connect(file_name: str, file_obj: List):
    excluded = ['CONECT', ]
    with open(file_name, 'w') as outfile:
        for index, line in enumerate(file_obj):
            if not any(s in line for s in excluded):
                outfile.write(line)


def remove_connects_from_file(structure_files: List):
    for pdb_file in structure_files:
        infile = open(pdb_file, 'r').readlines()
        remove_connect(file_name=f'{pdb_file[:-4]}_noconnect.pdb', file_obj=infile)


def run():
    ligand_structures = get_files(externals.DATA_PATH, ext='ligand_HH.pdb', ext_a='ligand_a_HH.pdb',
                                  ext_b='ligand_b_HH.pdb', given_dirs=list(externals.PDB_TO_DO.keys()))
    remove_connects_from_file(ligand_structures)


run()
