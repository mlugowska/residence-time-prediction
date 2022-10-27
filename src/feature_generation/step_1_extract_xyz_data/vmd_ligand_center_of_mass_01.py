import os
import traceback
from typing import List, Tuple

from vmd import molecule, evaltcl

from utils import externals

from utils.get_pdb_files import get_files


def get_prmtop_files() -> List[str]:
    return get_files(externals.DATA_PATH, ext='tip3_ions.prmtop', given_dirs=list(externals.VMD_PDB.keys()))


def get_dcd_file(replica: int, pdb_: str) -> List[Tuple[str, str, str]]:
    files = []
    for root, dirs, filenames in os.walk(f'{externals.MOUNT_ICM_PATH}/{pdb_}/{replica}'):
        for dir in dirs:
            for name in os.listdir(f'{root}/{dir}'):
                if name.endswith('dcd'):
                    files.append((root, dir, name))
    return files


def run() -> None:
    for prmtop_file in get_prmtop_files():
        pdb_id = prmtop_file[69:73]

        with open("log.txt", "w") as log:
            for replica_num in range(1, 6):
                dcd_files = get_dcd_file(replica=replica_num, pdb_=pdb_id)
                for dcd_file in dcd_files:
                    root, dir, name = dcd_file
                    try:
                        molid = molecule.load("parm7", prmtop_file)
                        molecule.read(molid, "dcd", f'{root}/{dir}/{name}', waitfor=-1)
                        evaltcl(f'source {externals.EXTRACT_LIGAND_COM_TCL}')
                        filename = f'{root}/{dir}/{name[:-4]}_COM.txt'
                        evaltcl(f'calculate_com {externals.VMD_PDB.get(pdb_id)} {filename}')
                        molecule.delete(molid)
                    except ValueError:
                        log.write(name)
                        traceback.print_exc(file=log)
                        continue


# run()
