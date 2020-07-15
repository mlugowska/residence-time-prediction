import os
from typing import List

import pandas as pd

from utils.externals import LIGAND_PATH, STRUCTURES_FILE
from utils.get_pdb_files import get_files

ligand_structures = get_files(os.path.join(LIGAND_PATH, 'protonated'), 'pdb')
os.chdir(os.getcwd())


def read_ligand_name(structures_file: str, pdb_file: str):
    df = pd.read_excel(structures_file)
    df['PDB ID'] = df.loc[:, 'PDB ID'].apply(lambda x: x.upper())
    row = df.loc[df['PDB ID'] == pdb_file[-18:-14]]
    return row['Ligand Code'].values[0]


def remove_conect(file_name: str, file_obj: object):
    with open(file_name, 'w') as outfile:
        for index, line in enumerate(file_obj):
            if 'CONECT' not in line:
                outfile.write(line)


def remove_connects_from_file(structure_files: List):
    for pdb_file in structure_files:
        infile = open(pdb_file, 'r').readlines()
        ligand_code = read_ligand_name(STRUCTURES_FILE, pdb_file)
        remove_conect(file_name=f'{pdb_file[:-14]}_{ligand_code}_noconnect.pdb', file_obj=infile)


def run():
    remove_connects_from_file(ligand_structures)
