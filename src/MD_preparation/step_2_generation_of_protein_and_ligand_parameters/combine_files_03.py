from typing import List

from src.MD_preparation.step_1_preparation_of_the_protein_and_ligand_structures.select_crystal_water_03 import \
    read_ligand_code
from src.utils import externals
from src.utils.get_pdb_files import get_files


def get_ligand_files(pdbs) -> [List[str]]:
    files = get_files(externals.DATA_PATH, ext='tleap.pdb', given_dirs=pdbs)
    min_length = min([len(x) for x in files])
    return list(filter(lambda x: len(x) < min_length + 2, files)), min_length


def get_protein_files(pdbs) -> List[str]:
    return get_files(externals.DATA_PATH, ext='protein.pdb', given_dirs=pdbs)


def get_water_files(pdbs) -> List[str]:
    return get_files(externals.DATA_PATH, ext='HOH_HH.pdb', given_dirs=pdbs)


def add_to_final_file(filename: str, output_filename: str, keyword: str, mode: str) -> None:
    infile = open(filename, 'r').readlines()
    with open(output_filename, mode) as outfile:
        for index, line in enumerate(infile):
            if keyword in line:
                outfile.write(line)


def add_protein(protein_file: str, output_filename: str) -> None:
    add_to_final_file(filename=f'{protein_file}',
                      output_filename=output_filename,
                      keyword='ATOM', mode='w')


def add_ligand(ligand_file: str, output_filename: str) -> None:
    add_to_final_file(filename=f'{ligand_file}',
                      output_filename=output_filename,
                      keyword=read_ligand_code(ligand_file), mode='a')


def add_water(water_file: str, output_filename: str) -> None:
    add_to_final_file(filename=f'{water_file}', output_filename=output_filename, keyword='HOH', mode='a')


def add_ter_line(output_filename: str) -> None:
    with open(output_filename, 'a') as outfile:
        outfile.write('TER \n')


def create_output_name(pdb: str, file: str, end: str) -> str:
    if pdb in externals.ab:
        return f'{file[:73]}_{file[-11:-10]}{end}'
    return f'{file[:73]}{end}'


def combine() -> None:
    '''
    Combine the protein, ligand, and crystallographic water PDB files into one file in which
    their coordinates are separated by TER lines:
    '''
    pdbs = list(externals.PDB_TO_DO.keys())
    protein_files = get_protein_files(pdbs)
    ligand_files, min_length = get_ligand_files(pdbs)
    water_files = get_water_files(pdbs)

    for pdb_ in pdbs:
        ligands = [file_ for file_ in ligand_files if pdb_ in file_]
        for ligand in ligands:
            protein = [file_ for file_ in protein_files if pdb_ in file_][0]
            water = [file_ for file_ in water_files if pdb_ in file_][0]
            output_name = create_output_name(pdb=pdb_, file=ligand, end='_final.pdb')

            add_protein(protein, output_name)
            add_ter_line(output_name)
            add_ligand(ligand, output_name)
            add_ter_line(output_name)
            add_water(water, output_name)


combine()
