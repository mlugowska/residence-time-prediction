from subprocess import call
from typing import List

from src.MD_preparation.step_2_generation_of_protein_and_ligand_parameters.combine_files_03 import get_ligand_files, \
    create_output_name
from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_tleap_input_file(complex_final: str, ligand_frcmod: str, ligand_lib: str, output_filename: str) -> None:
    '''
    output: tleap input file for generation of the topology and coordinate files of the complex
    '''

    with open(output_filename, "w") as f:
        lines = [
            f'source {externals.AMBER_FORCE_FIELD_PATH}/cmd/oldff/leaprc.ff14SB',
            f'source {externals.AMBER_FORCE_FIELD_PATH}/cmd/leaprc.gaff',
            f'loadamberparams {externals.AMBER_FORCE_FIELD_PATH}/parm/frcmod.ionsjc_tip3p',
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


def get_complex_file(pdb: str, ligand_file: str, complexes: List[str]) -> str:
    if pdb in externals.ab:
        return [complex_ for complex_ in complexes if complex_[-11:-10] == ligand_file[-11:-10]][0]
    return complexes[0]


def run() -> None:
    pdbs = list(externals.PDB_TO_DO.keys())
    ligand_files, min_length = get_ligand_files(pdbs=pdbs)
    complex_files = get_files(externals.DATA_PATH, ext='final.pdb', given_dirs=pdbs)

    for pdb_ in pdbs:
        ligands = [file_ for file_ in ligand_files if pdb_ in file_]
        complexes = [file_ for file_ in complex_files if pdb_ in file_]
        for ligand in ligands:
            complex_ = get_complex_file(pdb=pdb_, ligand_file=ligand, complexes=complexes)
            output_name = create_output_name(pdb=pdb_, file=complex_, end='_tleap_all_in')
            ligand_frcmod = f'{ligand[:-10]}.frcmod'
            ligand_lib = f'{ligand[:-10]}.lib'
            create_tleap_input_file(complex_final=complex_, ligand_frcmod=ligand_frcmod, ligand_lib=ligand_lib,
                                    output_filename=output_name)
            solvate_system_add_ions(output_name)


run()
