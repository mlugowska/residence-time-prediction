import os
from subprocess import call

from src.utils import externals
from src.utils.get_pdb_files import get_files


def convert(input_files, object):
    for file in input_files:
        output_name = os.path.join(file[:-16], f'{file[:-4]}.mol2')
        input_type = '-ipdb' if object == 'protein' else '-isdf'
        CMD = ['babel', input_type, file, '-omol2', output_name]
        call(CMD)


if __name__ == '__main__':
    pdbs = list(externals.PDB_TO_DO.keys())
    ligands = get_files(externals.DATA_PATH, ext='.sdf', given_dirs=pdbs)

    convert(ligands, 'ligand')
