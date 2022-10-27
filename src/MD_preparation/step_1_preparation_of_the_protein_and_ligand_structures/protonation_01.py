from typing import List

from pymol import cmd
from src.utils import externals
from src.utils.get_pdb_files import get_files


def get_structure_name_idx(structure_type: str, structure: str):
    if structure_type == 'ligand' and structure[-22:-18] in externals.ab:
        return [-17, -4]
    elif structure_type == 'protein':
        return [-16, -5]
    return [-15, -5]


def protonate_structures(structure_files: List, structure_type: str):
    for structure in structure_files:
        cmd.load(structure)
        selection = f'{structure[get_structure_name_idx(structure_type, structure)[0]:get_structure_name_idx(structure_type, structure)[1]]}'
        cmd.h_add(selection=selection)
        cmd.save(f'{structure[:-4]}_HH.pdb', selection)
        cmd.delete(f'{structure}')


def rename_ligand(ligand_files: str):
    '''
    needs to be reimplemented
    '''
    for ligand_file in ligand_files:
        infile = open(ligand_file, 'r').readlines()
        with open(ligand_file, 'w') as outfile:
            for index, line in enumerate(infile):
                line = line.replace('UNK', f'{ligand_file[-10:-7]}')
                outfile.write(line)


def run():
    pdbs = list(externals.PDB_TO_DO.keys())
    protein_structures = get_files(externals.DATA_PATH, ext='protein.pdb', given_dirs=pdbs)
    ligand_structures = get_files(externals.DATA_PATH, ext='ligand.pdb', ext_a='ligand_a.pdb', ext_b='ligand_b.pdb',
                                  given_dirs=pdbs)

    protonate_structures(ligand_structures, 'ligand')
    protonate_structures(protein_structures,  'protein')

    # ligand_files = get_files(externals.LIGAND_PATH, '.pdb')
    # rename_ligand(ligand_files)


run()
