import os
from subprocess import call

from utils.externals import LIGAND_PATH
from utils.get_pdb_files import get_files


def convert(input_files, object):
    for file in input_files:
        output_name = os.path.join(file[:-16], f'{file[:-4]}.mol2')
        input_type = '-ipdb' if object == 'protein' else '-isdf'
        CMD = ['babel', input_type, file, '-omol2', output_name]
        call(CMD)


if __name__ == '__main__':
    # proteins = get_files(PROTEIN_PATH, '.pdb')
    ligands = get_files(LIGAND_PATH, '.sdf')

    # convert(proteins, 'protein')
    convert(ligands, 'ligand')
