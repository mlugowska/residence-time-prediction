from subprocess import call

from src.utils import externals
from src.utils.get_pdb_files import get_files


def convert(ligand_pdb: str, output_filename: str):
    # the ligand net charge is very general and equal to 0 - it'd be better to use some external tool to calculate
    # nc parameter for each ligand
    cmd = ['antechamber', '-i', f'{ligand_pdb}', '-fi', 'pdb', '-o', f'{output_filename}', '-fo', 'mol2', '-c', 'bcc',
           '-s', '2']
    call(cmd)


def rename_ligand(mol2_file: str):
    infile = open(mol2_file, 'r').readlines()
    with open(mol2_file, 'w') as outfile:
        for index, line in enumerate(infile):
            line = line.replace('UNK', f'{mol2_file[-21:-18]}')
            outfile.write(line)


def run():
    ligand_files = get_files(externals.LIGAND_PATH, '_HH_noconnect.mol2')
    for pdb_ in ligand_files:
        convert(pdb_, f'{pdb_[:-4]}.mol2')
        try:
            rename_ligand(f'{pdb_[:-4]}.mol2')
        except FileNotFoundError:
            # antechamber -j 5 -at sybyl -dr no -i 5LNZ_ligand_HH_noconnect.pdb -fi pdb -o 5LNZ_70Z_HH_noconnect.mol2 -fo mol2
            pass


run()
