import os
from typing import List, Tuple

from utils import externals
from utils.get_pdb_files import get_md_files


def get_times(pdb_id: str, path: str, rep_num: int, files: List[str]) -> None:
    """
    grep  "LIGAND EXIT EVENT DETECTED" */*out > times_1.dat
    """
    for file in files:
        filename = f'{pdb_id}_times_{rep_num}.dat'
        cmd = f'grep "LIGAND EXIT EVENT DETECTED" {file} >> {path}/{filename}'
        os.system(cmd)


def get_path_to_ramd(pdb_id: str, rep_num: int) -> Tuple[str, str]:
    if pdb_id in externals.ab:
        return f'{externals.MOUNT_ICM_PATH}/{pdb_id}/A/{rep_num}', f'{externals.MOUNT_ICM_PATH}/{pdb_id}/B/{rep_num}'
    return f'{externals.MOUNT_ICM_PATH}/{pdb_id}/{rep_num}', ''


def create_times_file(pdb_id: str, rep_num: int, path: str) -> None:
    outs = {rep_num: get_md_files(path, '014.log')}
    outs.get(rep_num).sort()
    get_times(pdb_id, path, rep_num, outs.get(rep_num))


def remove_dat_file(path: str) -> None:
    for item in os.listdir(path):
        if item.endswith(".dat"):
            os.remove(os.path.join(path, item))


def run() -> None:
    pdbs = list(externals.VMD_PDB.keys())
    for pdb_id in pdbs:
        for rep_num in range(4, 6):
            print(pdb_id, rep_num)
            path, path_ab = get_path_to_ramd(pdb_id, rep_num)
            remove_dat_file(path)
            create_times_file(pdb_id, rep_num, path)
            if path_ab:
                remove_dat_file(path_ab)
                create_times_file(pdb_id, rep_num, path_ab)


run()
