import os

from src.utils import externals as externals
from src.utils.get_pdb_files import get_files


def generate_parameter_files() -> None:
    ligand_files = get_files(os.path.join(externals.LIGAND_PATH, 'protonated'), 'mol2')
    for ligand_file in ligand_files:
        file_path = f'{ligand_file[:-23]}{ligand_file[-23:-15]}'
        file_name = f'{ligand_file[-23:]}'
        # determine_bond_and_atom_types(f'{file_path}/{file_name}', f'{file_path}/{ligand_file[-23:-15]}.frcmod')

        # create_tleap_input_ligand_file(file_path)
        # generate_topology_coordinate_pdb_files(f'{file_path}/{file_path[-8:]}_tleap_ligand_in')
