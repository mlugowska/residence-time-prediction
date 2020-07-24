from subprocess import call

from src.MD_preparation.step_2_generation_of_protein_and_ligand_parameters.create_complex_03 import get_ligand_files


def create_tleap_input_file(complex_path: str) -> None:
    '''
    output: tleap input file for generation of the topology and coordinate files of the complex
    '''

    files, ligand_dirs = get_ligand_files()

    with open(f'{complex_path}/{file_path[-8:]}_tleap_ligand_in', "w") as f:
        lines = [
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/oldff/leaprc.ff14SB',
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/leaprc.gaff',
            '/Users/mlugowska/PhD/tools/amber20/dat/leap/parm/frcmod.ionsjc_tip3p'
            f'loadamberparams {ligand_frcmod}', f'loadoff {ligand_lib}', f'complex  = loadpdb {complex_final}',
            'solvateBox complex TIP3PBOX 10', 'charge complex', 'addionsrand complex Na+ 31 Cl- 24', 'charge complex',
            f'saveamberparm complex {ref}.prmtop {ef}.inpcrd', f'savepdb complex {ref}.pdb', 'quit'
        ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def solvate_system_add_ions(tleap_all_in: str) -> None:
    '''
    tleap_all_in: created in create_tleap_input_file()
    output: topology (X.prmtop), PDB (X.pdb) and coordinate (X.impcrd) files in Amber format
    '''
    cmd = ['tleap', '-f', f'{tleap_all_in}']
    call(cmd)
    pass

# TODO: create_tleap_input_file i solvate_system_add_ions przyjmuje 1 strukturę - zrobić metodę, która iteruje po wszystkich i wywołuje te 2
