import os
from subprocess import call
from typing import List, Union

from src.MD_preparation.step_2_generation_of_protein_and_ligand_parameters.combine_files_03 import get_ligand_files, \
    get_pdbs
from src.utils import externals
from src.utils.get_pdb_files import get_files


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


def run() -> None:
    ligand_files, min_length = get_ligand_files()
    complex_files = get_files(externals.COMPLEX_PATH, 'final.pdb')

    for pdb_ in get_pdbs(ligand_files, min_length):
        ligands = [file_ for file_ in ligand_files if pdb_ in file_]
        complexes = [file_ for file_ in complex_files if pdb_ in file_]
        for ligand in ligands:
            if len(ligands) == 1:
                complex_ = complexes[0]
            else:
                complex_ = [complexes[idx] for idx, match in enumerate(complexes) if match[-19:-10] == ligand[-13:-4]][0]
            ligand_frcmod = f'{ligand[:-4]}.frcmod'
            ligand_lib = f'{ligand[:-4]}.lib'
            create_tleap_input_file(complex_final=complex_, ligand_frcmod=ligand_frcmod, ligand_lib=ligand_lib,
                                    output_filename=f'{complex_[:-10]}_tleap_all_in')
            solvate_system_add_ions(f'{complex_[:-10]}_tleap_all_in')


run()
