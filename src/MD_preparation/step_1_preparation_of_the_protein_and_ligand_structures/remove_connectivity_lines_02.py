from typing import List

import pandas as pd

from src.utils import externals
from src.utils.get_pdb_files import get_files


def read_ligand_name(structures_file: str, pdb_file: str):
    df = pd.read_excel(structures_file)
    df['PDB ID'] = df.loc[:, 'PDB ID'].apply(lambda x: x.upper())
    row = df.loc[df['PDB ID'] == pdb_file[-18:-14]]
    return row['Ligand Code'].values[0]


def remove_connect(file_name: str, file_obj: List):
    excluded = ['Cl', 'CL', 'CONECT']
    with open(file_name, 'w') as outfile:
        for index, line in enumerate(file_obj):
            if not any(s in line for s in excluded):
                outfile.write(line)


def remove_connects_from_file(structure_files: List):
    for pdb_file in structure_files:
        infile = open(pdb_file, 'r').readlines()
        ligand_code = read_ligand_name(externals.STRUCTURES_FILE, pdb_file)
        remove_connect(file_name=f'{pdb_file[:-14]}_{ligand_code}_HH_noconnect.pdb', file_obj=infile)


def run():
    ligand_structures = get_files(externals.LIGAND_PATH, '_HH.pdb')
    remove_connects_from_file(ligand_structures)


run()
