import os
from typing import List

from src.utils.get_pdb_files import get_files


def get_times(path: str, rep_num: int, files: List[str]):
    '''
    grep  "LIGAND EXIT EVENT DETECTED" */*out > times_1.dat
    '''
    for file in files:
        filename = f'{path[-11:-7]}_times_{rep_num}.dat'
        cmd = f'grep "LIGAND EXIT EVENT DETECTED" {file} >> {path}/{filename}'
        os.system(cmd)


def run():
    # TODO: handle paths to all complexes' ramd outputs
    outs = {}
    for rep_num in range(1,6):
        PATH = f'/Users/mlugowska/PhD/residence-time-prediction/data/complex_files/1XKK/ramd/{rep_num}'
        outs[rep_num] = get_files(PATH, '.out')
        get_times(PATH, rep_num, outs.get(rep_num))


run()
