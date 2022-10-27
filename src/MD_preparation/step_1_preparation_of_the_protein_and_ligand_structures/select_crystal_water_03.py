from typing import List

from pymol import cmd

from src.utils import externals
from src.utils.get_pdb_files import get_files


def read_ligand_code(pdb_file: str):
    return externals.PDB_TO_DO.get(pdb_file[64:68])


def select_water_residue(structure_files: List, dist=None):
    for structure in structure_files:
        cmd.load(structure)
        selection = f'{structure[-8:-4]}_water'
        cmd.select(selection, f'resname HOH within {dist} of resname {read_ligand_code(structure)}')
        cmd.save(f'{structure[:-4]}_HOH.pdb', selection)


def run():
    pdbs = list(externals.PDB_TO_DO.keys())
    complex_structures = get_files(externals.DATA_PATH, type_='complex', given_dirs=pdbs, ext='.pdb')
    select_water_residue(structure_files=complex_structures, dist=5)


run()
