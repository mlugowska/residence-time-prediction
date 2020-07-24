from subprocess import call

from src.utils.get_pdb_files import get_files


def create_tleap_input_ligand_file(file_path: str) -> None:
    ligand_file_mol2 = get_files(file_path, 'mol2')[0]
    ligand_file_frcmod = get_files(file_path, 'frcmod')[0]
    with open(f'{file_path}/{file_path[-8:]}_tleap_ligand_in', "w") as f:
        lines = [
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/oldff/leaprc.ff14SB',
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/leaprc.gaff',
            f'LIG = loadmol2 {ligand_file_mol2}', 'check LIG', f'loadamberparams {ligand_file_frcmod}',
            f'saveoff LIG {ligand_file_frcmod[:-7]}.lib',
            f'saveamberparm LIG {ligand_file_frcmod[:-7]}.prmtop {ligand_file_frcmod[:-7]}.inpcrd',
            f'savepdb LIG {ligand_file_frcmod[:-7]}.pdb', 'charge LIG', 'quit'

        ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def create(tleap_ligand_in: str) -> None:
    '''
    tleap_ligand_in: tleap input file for generation of the ligand parameters
    :return:
    '''

    cmd = ['tleap', '-f', f'{tleap_ligand_in}']
    call(cmd)
