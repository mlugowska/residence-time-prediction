from subprocess import call

from src.MD_preparation.step_1_preparation_of_the_protein_and_ligand_structures.select_crystal_water_03 import \
    read_ligand_code
from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_tleap_input_ligand_file(mol2_file: str, frcmod_file: str, code: str, output_filename: str,
                                   frcmod_idx: int) -> None:
    with open(output_filename, "w") as f:
        lines = [
            f'source {externals.AMBER_FORCE_FIELD_PATH}/cmd/oldff/leaprc.ff14SB',
            f'source {externals.AMBER_FORCE_FIELD_PATH}/cmd/leaprc.gaff',
            f'{code} = loadmol2 {mol2_file}', f'check {code}', f'loadamberparams {frcmod_file}',
            f'saveoff {code} {frcmod_file[:frcmod_idx]}.lib',
            f'saveamberparm {code} {frcmod_file[:frcmod_idx]}.prmtop {frcmod_file[:frcmod_idx]}.inpcrd',
            f'savepdb {code} {frcmod_file[:frcmod_idx]}_tleap.pdb', f'charge {code}', 'quit'
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


def get_output_name_idx(structure: str):
    if structure[64:68] in externals.ab:
        return [69, 82]
    return [69, 80]


def run() -> None:
    pdbs = list(externals.PDB_TO_DO.keys())
    ligand_files = get_files(externals.DATA_PATH, ext='mol2', given_dirs=pdbs)
    frcmod_files = get_files(externals.DATA_PATH, ext='frcmod', given_dirs=pdbs)

    for frcmod_file in frcmod_files:
        idx_min = get_output_name_idx(frcmod_file)[0]
        idx_max = get_output_name_idx(frcmod_file)[1]
        ligand_file = [
            ligand_file for ligand_file in ligand_files if ligand_file[idx_min:idx_max] == frcmod_file[idx_min:idx_max]
        ][0]
        output_filename = f'{ligand_file[:-18]}_tleap_ligand_in'
        create_tleap_input_ligand_file(mol2_file=ligand_file, frcmod_file=frcmod_file,
                                       code=read_ligand_code(frcmod_file),
                                       output_filename=output_filename, frcmod_idx=-7)
        calculate_ligand_parameters(output_filename)


run()
