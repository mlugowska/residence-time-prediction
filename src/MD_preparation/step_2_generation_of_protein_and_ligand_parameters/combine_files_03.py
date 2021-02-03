import os
from typing import List

from src.utils import externals
from src.utils.get_pdb_files import get_files


def get_ligand_files() -> [List[str]]:
    files = get_files(externals.LIGAND_PATH, 'BAW.pdb')
    min_length = min([len(x) for x in files])
    return list(filter(lambda x: len(x) < min_length + 2, files)), min_length


def get_protein_files() -> List[str]:
    return get_files(externals.PROTEIN_PATH, 'protein.pdb')


def get_water_files() -> List[str]:
    return get_files(os.path.join(externals.COMPLEX_PATH, 'crystallographic_hoh_hh'), 'pdb')


def get_pdbs(ligand_files: List[str], length: int) -> List[str]:
    pdbs = []
    for file in ligand_files:
        if len(file) == length:
            pdbs.append(file[-12:-8])
        else:
            pdbs.append(file[-13:-9])
    return list(set(pdbs))


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
                      keyword=f'{ligand_file[-7:-4]}', mode='a')


def add_water(water_file: str, output_filename: str) -> None:
    add_to_final_file(filename=f'{water_file}', output_filename=output_filename, keyword='HOH', mode='a')


def add_ter_line(output_filename: str) -> None:
    with open(output_filename, 'a') as outfile:
        outfile.write('TER \n')


def combine() -> None:
    '''
    Combine the protein, ligand, and crystallographic water PDB files into one file in which
    their coordinates are separated by TER lines:
    '''

    protein_files = get_protein_files()
    ligand_files, min_length = get_ligand_files()
    water_files = get_water_files()

    for pdb_ in get_pdbs(ligand_files, min_length):
        ligands = [file_ for file_ in ligand_files if pdb_ in file_]
        for ligand in ligands:
            protein = [file_ for file_ in protein_files if pdb_ in file_][0]
            water = [file_ for file_ in water_files if pdb_ in file_][0]
            if len(ligands) == 1:
                output_filename = os.path.join(externals.COMPLEX_PATH, f'{pdb_}', f'{ligand[-12:-4]}_final.pdb')
            else:
                output_filename = os.path.join(externals.COMPLEX_PATH, f'{pdb_}', f'{ligand[-13:-4]}_final.pdb')
            add_protein(protein, output_filename)
            add_ter_line(output_filename)
            add_ligand(ligand, output_filename)
            add_ter_line(output_filename)
            add_water(water, output_filename)


combine()
