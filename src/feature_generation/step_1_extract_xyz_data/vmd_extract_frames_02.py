import os
import traceback

from vmd import molecule, evaltcl

from vmd_ligand_center_of_mass_01 import get_prmtop_files, get_dcd_file
from utils import externals


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

                        evaltcl(f'source {externals.EXTRACT_FRAMES_PDB_TCL}')

                        os.makedirs(f'{root}/{dir}/pdbs/')

                        filename = f'{root}/{dir}/pdbs/{pdb_id}_{replica_num}'
                        evaltcl(f'extract_frames {filename}')
                        molecule.delete(molid)
                    except ValueError:
                        log.write(name)
                        traceback.print_exc(file=log)
                        continue


run()
