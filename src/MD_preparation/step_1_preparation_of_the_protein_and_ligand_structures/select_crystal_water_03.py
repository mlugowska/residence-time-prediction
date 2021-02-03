import os
from typing import List

from pymol import cmd

from src.utils import externals
from src.utils.get_pdb_files import get_files


def read_ligand_code(files: List, structure: str):
    for file in files:
        if structure[-8:-4] in file:
            print(file[-20:-17])
            return file[-20:-17]


def select_water_residue(structure_files: List, complex_path: str, ligand_files: List, dist=None):
    for structure in structure_files:
        cmd.load(structure)
        cmd.select(f'{structure[-8:-4]}_water',
                   f'resname HOH within {dist} of resname {read_ligand_code(ligand_files, structure)}')
        output_path = os.path.join(complex_path, 'crystallographic_hoh')
        output_file = os.path.join(output_path, f'{structure[-8:-4]}_HOH.pdb')

        cmd.save(output_file, f'{structure[-8:-4]}_water')


def run():
    ligand_structures = get_files(externals.LIGAND_PATH, 'HH_noconnect.pdb')
    complex_structures = get_files(externals.COMPLEX_PATH, '.pdb')
    select_water_residue(structure_files=complex_structures, complex_path=externals.COMPLEX_PATH,
                         ligand_files=ligand_structures, dist=5)


run()
