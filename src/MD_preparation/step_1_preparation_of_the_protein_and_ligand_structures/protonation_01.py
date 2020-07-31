import os
from typing import List

from pymol import cmd
from src.utils import externals
from src.utils.get_pdb_files import get_files


def protonate_structures(structure_files: List, structure_type: str):
    if structure_type == 'protein':
        structure_name_idx = [-16, -4]
    else:
        structure_name_idx = [-15, -4]

    for structure in structure_files:
        cmd.load(structure)
        cmd.h_add(selection=f'({structure[structure_name_idx[0]:structure_name_idx[1]]})')
        cmd.save(os.path.join(structure[:-20], f'{structure[structure_name_idx[0]:structure_name_idx[1]]}_HH.pdb'),
                 f'({structure[structure_name_idx[0]:structure_name_idx[1]]})')
        cmd.delete(f'{structure}')


def run():
    protein_structures = get_files(externals.PROTEIN_PATH, 'pdb')
    ligand_structures = get_files(externals.LIGAND_PATH, 'sdf')

    protonate_structures(ligand_structures, 'ligand')
    protonate_structures(protein_structures,  'protein')


run()
