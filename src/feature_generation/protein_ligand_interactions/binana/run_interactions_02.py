import os
from subprocess import call

from src.utils.externals import BINANA_PATH, PROTEIN_PATH, LIGAND_PATH, OUTPUT_PATH
from src.utils.get_pdb_files import get_files


def run_binana(protein_files, ligand_files, output_path):
    for protein_file in protein_files:
        ligand_file = [file for file in ligand_files if protein_file[-18:-14] in file][0]
        output_dir = os.path.join(output_path, f'{protein_file[-18:-14]}')
        os.makedirs(output_dir)
        CMD = ['python', BINANA_PATH, '-receptor', protein_file, '-ligand',
               ligand_file, '-output_dir', output_dir]
        call(CMD)


if __name__ == '__main__':
    protein_files = get_files(PROTEIN_PATH, '.pdbqt')
    ligand_files = get_files(LIGAND_PATH, '.pdbqt')

    run_binana(protein_files, ligand_files, OUTPUT_PATH)
