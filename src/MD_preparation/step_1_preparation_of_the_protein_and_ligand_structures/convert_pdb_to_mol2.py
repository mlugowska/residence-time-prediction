import os
from subprocess import call

from src.utils.externals import LIGAND_PATH
from src.utils.get_pdb_files import get_files


def convert(ligand_pdb: str, output_filename: str):
    # the ligand bet charge is very general and equal to 0 - it'd be better to use some external tool to calculate
    # nc parameter for each ligand
    cmd = ['antechamber', '-i', f'{ligand_pdb}', '-fi', 'pdb', '-o', f'{output_filename}', '-fo', 'mol2', '-c', 'bcc',
           '-s', '2']
    call(cmd)


def rename_ligand(mol2_file: str):
    infile = open(mol2_file, 'r').readlines()
    with open(mol2_file, 'w') as outfile:
        for index, line in enumerate(infile):
            line = line.replace('UNK', f'{mol2_file[-18:-15]}')
            outfile.write(line)


def run():
    ligand_files = get_files(os.path.join(LIGAND_PATH, 'protonated'), 'noconnect.pdb')
    for pdb_ in ligand_files:
        convert(pdb_, f'{pdb_[:-14]}/{pdb_[-22:-4]}.mol2')
        if os.listdir(f'{pdb_[:-14]}'):
            rename_ligand(f'{pdb_[:-14]}/{pdb_[-22:-4]}.mol2')


run()
