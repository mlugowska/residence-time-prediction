import os
from subprocess import call
from typing import List, Union

from src.MD_preparation.step_2_generation_of_protein_and_ligand_parameters.combine_files_03 import get_ligand_files, \
    get_pdbs
from src.utils import externals


def create_tleap_input_file(complex_final: str, ligand_frcmod: str, ligand_lib: str, output_filename: str) -> None:
    '''
    output: tleap input file for generation of the topology and coordinate files of the complex
    '''

    with open(output_filename, "w") as f:
        lines = [
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/oldff/leaprc.ff14SB',
            'source /Users/mlugowska/PhD/tools/amber20/dat/leap/cmd/leaprc.gaff',
            'loadamberparams /Users/mlugowska/PhD/tools/amber20/dat/leap/parm/frcmod.ionsjc_tip3p',
            f'loadamberparams {ligand_frcmod}', f'loadoff {ligand_lib}', f'complex  = loadpdb {complex_final}',
            'solvateBox complex TIP3PBOX 10', 'charge complex', 'addions complex Na+ 0', 'addions complex Cl- 0',
            'charge complex',
            f'saveamberparm complex {complex_final[:-10]}_tip3_ions.prmtop {complex_final[:-10]}_tip3_ions.inpcrd',
            f'savepdb complex {complex_final[:-10]}_tip3_ions.pdb', 'quit'
        ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def solvate_system_add_ions(tleap_all_in: str) -> None:
    '''
    tleap_all_in: created in create_tleap_input_file()
    output: topology (X.prmtop), PDB (X.pdb) and coordinate (X.inpcrd) files in Amber format
    '''
    cmd = ['tleap', '-f', f'{tleap_all_in}']
    call(cmd)


def get_complex_files() -> List[Union[str, bytes]]:
    finals = []
    for root, dirs, filenames in os.walk(externals.COMPLEX_PATH):
        for dir in dirs:
            for filename in filenames:
                if filename.endswith('final.pdb'):
                    finals.append(os.path.join(root, dir, filename))
        return finals


def run() -> None:
    ligand_files, ligand_dirs = get_ligand_files()
    complex_files = get_complex_files()

    for pdb_ in get_pdbs(ligand_files):
        complex_ = [file_ for file_ in complex_files if pdb_ in file_][0]
        ligand_dir = [dir for dir in ligand_dirs if pdb_ in dir][0]
        ligand_frcmod = os.path.join(ligand_dir,
                                     [file_ for file_ in os.listdir(ligand_dir) if file_.endswith('frcmod')][0])
        ligand_lib = os.path.join(ligand_dir, [file_ for file_ in os.listdir(ligand_dir) if file_.endswith('lib')][0])

        create_tleap_input_file(complex_final=complex_, ligand_frcmod=ligand_frcmod, ligand_lib=ligand_lib,
                                output_filename=f'{complex_[:-10]}_tleap_all_in')
        solvate_system_add_ions(f'{complex_[:-10]}_tleap_all_in')


run()
