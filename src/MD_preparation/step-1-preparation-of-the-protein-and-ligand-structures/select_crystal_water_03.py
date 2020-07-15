import os
from typing import List

from pymol import cmd

from utils.externals import COMPLEX_PATH, LIGAND_PATH
from utils.get_pdb_files import get_files


def read_ligand_code(files: List, structure: str):
    for file in files:
        if structure[-8:-4] in file:
            print(file[-17:-14])
            return file[-17:-14]


def select_water_residue(structure_files: List, complex_path: str, ligand_files: List, dist=None):
    for structure in structure_files:
        cmd.load(structure)
        cmd.select(f'{structure[-8:-4]}_water',
                   f'resname HOH within {dist} of resname {read_ligand_code(ligand_files, structure)}')
        output_path = os.path.join(complex_path, 'crystallographic_hoh')
        output_file = os.path.join(output_path, f'{structure[-8:-4]}_HOH.pdb')

        cmd.save(output_file, f'{structure[-8:-4]}_water')


def run():
    ligand_structures = get_files(os.path.join(LIGAND_PATH, 'protonated'), 'pdb')
    files = []
    for file in ligand_structures:
        if 'noconnect' in file:
            files.append(file)
    complex_structures = get_files(COMPLEX_PATH, 'pdb')
    select_water_residue(structure_files=complex_structures, complex_path=COMPLEX_PATH, ligand_files=files, dist=5)


run()