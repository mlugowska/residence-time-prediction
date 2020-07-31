import os
from subprocess import call

from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_tleap_input_ligand_file(file_path: str, code: str) -> None:
    ligand_file_mol2 = get_files(file_path, 'mol2')[0]
    ligand_file_frcmod = get_files(file_path, 'frcmod')[0]
    with open(f'{file_path}/{file_path[-8:]}_tleap_ligand_in', "w") as f:
        lines = [
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/oldff/leaprc.ff14SB',
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/leaprc.gaff',
            f'{code} = loadmol2 {ligand_file_mol2}', f'check {code}', f'loadamberparams {ligand_file_frcmod}',
            f'saveoff {code} {ligand_file_frcmod[:-7]}.lib',
            f'saveamberparm {code} {ligand_file_frcmod[:-7]}.prmtop {ligand_file_frcmod[:-7]}.inpcrd',
            f'savepdb {code} {ligand_file_frcmod[:-7]}.pdb', f'charge {code}', 'quit'

        ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def calculate_ligand_parameters(tleap_ligand_in: str) -> None:
    '''
    tleap_ligand_in: tleap input file for generation of the ligand parameters
    :return:
    '''

    cmd = ['tleap', '-f', f'{tleap_ligand_in}']
    call(cmd)


def run() -> None:
    ligand_files = get_files(os.path.join(externals.LIGAND_PATH, 'protonated'), 'mol2')
    for ligand_file in ligand_files:
        file_path = f'{ligand_file[:-23]}{ligand_file[-23:-15]}'
        ligand_code = file_path[-3:]

        create_tleap_input_ligand_file(file_path, ligand_code)
        calculate_ligand_parameters(f'{file_path}/{file_path[-8:]}_tleap_ligand_in')


run()
