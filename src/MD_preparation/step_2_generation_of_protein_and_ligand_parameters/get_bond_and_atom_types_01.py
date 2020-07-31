import os
from subprocess import call

from src.utils import externals
from src.utils.get_pdb_files import get_files


def determine_bond_and_atom_types(ligand_mol2: str, output_filename: str) -> None:
    '''
    Determine the bond and atom types of the ligand
    '''

    cmd = ['parmchk2', '-i', f'{ligand_mol2}', '-f', 'mol2', '-o', f'{output_filename}']
    call(cmd)


def run() -> None:
    ligand_files = get_files(externals.LIGAND_PATH, 'HH_noconnect.mol2')
    for ligand_file in ligand_files:
        file_path = f'{ligand_file[:-23]}{ligand_file[-23:-18]}'
        file_name = f'{ligand_file[-23:]}'
        determine_bond_and_atom_types(f'{file_path}/{file_name}', f'{file_path}/{ligand_file[-23:-18]}.frcmod')
