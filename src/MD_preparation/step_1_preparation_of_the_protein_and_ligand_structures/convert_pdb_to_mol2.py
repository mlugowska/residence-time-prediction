from subprocess import call

from src.utils import externals
from src.utils.get_pdb_files import get_files


def convert(ligand_pdb: str, output_filename: str):
    # the ligand net charge is very general and equal to 0 - it'd be better to use some external tool to calculate
    # nc parameter for each ligand
    cmd = ['antechamber', '-i', f'{ligand_pdb}', '-fi', 'pdb', '-o', f'{output_filename}', '-fo', 'mol2', '-c', 'bcc',
           '-s', '2']
    call(cmd)


def run():
    ligand_files = get_files(externals.LIGAND_PATH, '72Y_HH_noconnect.pdb')
    for pdb_ in ligand_files:
        convert(pdb_, f'{pdb_[:-4]}.mol2')


run()
