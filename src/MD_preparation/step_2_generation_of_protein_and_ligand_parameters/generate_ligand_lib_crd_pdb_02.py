from subprocess import call

from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_tleap_input_ligand_file(mol2_file: str, frcmod_file: str, code: str, output_filename: str,
                                   frcmod_idx: int) -> None:
    with open(output_filename, "w") as f:
        lines = [
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/oldff/leaprc.ff14SB',
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/leaprc.gaff',
            f'{code} = loadmol2 {mol2_file}', f'check {code}', f'loadamberparams {frcmod_file}',
            f'saveoff {code} {frcmod_file[:frcmod_idx]}.lib',
            f'saveamberparm {code} {frcmod_file[:frcmod_idx]}.prmtop {frcmod_file[:frcmod_idx]}.inpcrd',
            f'savepdb {code} {frcmod_file[:frcmod_idx]}.pdb', f'charge {code}', 'quit'
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
    ligand_files = get_files(externals.LIGAND_PATH, 'mol2')
    ab_conformations = ['6EYA', '5UGS', '5LNZ', '6DJ1', '2YKJ', '5J2X']
    for ligand_file in ligand_files:
        if ligand_file[-35:-31] == '5LR1':

            if ligand_file[-36:-32] in ab_conformations:
                file_path = ligand_file[:-28]
                frcmod_files = get_files(ligand_file[:-28], 'frcmod')
            else:
                file_path = ligand_file[:-27]
                frcmod_files = get_files(ligand_file[:-27], 'frcmod')

            ligand_code = file_path[-3:]

            for frcmod_file in frcmod_files:
                output_filename = f'{ligand_file[:-18]}_tleap_ligand_in'
                create_tleap_input_ligand_file(mol2_file=ligand_file, frcmod_file=frcmod_file, code=ligand_code,
                                               output_filename=output_filename, frcmod_idx=-7)
                calculate_ligand_parameters(output_filename)


run()
