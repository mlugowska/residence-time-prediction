import matplotlib.pyplot as plt
import numpy as np

from src.utils import externals
from src.utils.get_pdb_files import get_files


def check_heat_or_equil(file: str):
    if 'heat' in file[-18:-13]:
        return 'heat'
    return 'equil'


def draw_plot():
    lig_dat = get_files(externals.COMPLEX_PATH, '-lig_rmsd.dat')
    prot_dat = get_files(externals.COMPLEX_PATH, '-prot_rmsd.dat')
    ab_conformations = ['6EYA', '5UGS', '5LNZ', '6DJ1', '2YKJ', '5J2X']

    for prot_file in prot_dat:
        if prot_file[66:70] in ab_conformations:
            output_path = prot_file[:87]
            idx = [-28, -14]
        else:
            output_path = prot_file[:85]
            idx = [-28, -15]

        lig_file = [lig for lig in lig_dat if prot_file[idx[0]:idx[1]] in lig][0]
        plt.plot(*np.loadtxt(lig_file, unpack=True), 'b-', linewidth=2.0)
        plt.plot(*np.loadtxt(prot_file, unpack=True), 'r-', linewidth=2.0)
        plt.xlabel('time [ps]')
        plt.ylabel('rmsd')
        plt.title(f'{prot_file[66:70]} {check_heat_or_equil(prot_file)} RMSD')
        plt.legend(['ligand', 'protein'])
        plt.savefig(f'{output_path}{prot_file[66:70]}_{check_heat_or_equil(prot_file)}.png')
        plt.clf()


draw_plot()
