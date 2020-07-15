import os
from typing import List

from pymol import cmd
from utils.externals import PROTEIN_PATH, LIGAND_PATH
from utils.get_pdb_files import get_files

protein_structures = get_files(PROTEIN_PATH, 'pdb')
ligand_structures = get_files(LIGAND_PATH, 'sdf')
os.chdir(os.getcwd())


def protonate_structures(structure_files: List, path: str, structure_type: str):
    if structure_type == 'protein':
        structure_name_idx = [-16, -4]
    else:
        structure_name_idx = [-15, -4]

    for structure in structure_files:
        cmd.load(structure)
        cmd.h_add(selection=f'({structure[structure_name_idx[0]:structure_name_idx[1]]})')
        cmd.save(os.path.join(path, 'protonated', f'{structure[structure_name_idx[0]:structure_name_idx[1]]}_HH.pdb'),
                 f'({structure[structure_name_idx[0]:structure_name_idx[1]]})')
        cmd.delete(f'{structure}')


def run():
    protonate_structures(ligand_structures, LIGAND_PATH, 'ligand')
#     protonate_structures(protein_structures, PROTEIN_PATH, 'protein')
