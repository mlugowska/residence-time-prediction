import os
from typing import Tuple, List

from utils import externals
from utils.get_pdb_files import get_files


def create_bash_file(content: List[str], output_filename: str) -> None:
    with open(output_filename, "w") as f:
        for line_ in content:
            f.writelines(line_)
            f.writelines('\n')


def create_batch_file(batch_filename: str, job_name: str, slurm_out: str, command: str) -> None:
    with open(batch_filename, "w") as f:
        lines = [
            '#!/bin/bash -l', f'#SBATCH -J {job_name}', '#SBATCH --nodes=6', '#SBATCH --ntasks-per-node=14',
            '#SBATCH --cpus-per-task=2', '#SBATCH --account=g85-918',
            '#SBATCH --partition=okeanos', f'#SBATCH --output="{slurm_out}"',

            'module load apps/ambertools/20',
            f'{command}'
        ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def get_protein_range(complex_file: str) -> Tuple[int, int]:
    infile = open(complex_file, 'r').readlines()
    first = int(infile[1][25])
    with open(complex_file, "r") as f:
        previous_line = ''
        for index, line in enumerate(infile):
            if 'TER' in line:
                last = int(previous_line[23:26])
                break
            previous_line = line
        return first, last


def create_dir(path: str, name: str) -> None:
    try:
        os.chdir(path)
        os.makedirs(name=name)
    except OSError:
        pass


def run() -> None:
    pdbs = list(externals.PDB_TO_DO.keys())
    prmtop_files = get_files(externals.DATA_PATH, ext='tip3_ions.prmtop', given_dirs=pdbs)
    inpcrd_files = get_files(externals.DATA_PATH, ext='tip3_ions.inpcrd', given_dirs=pdbs)
    pdb_files = get_files(externals.DATA_PATH, ext='tip3_ions.pdb', given_dirs=pdbs)

    for prmtop_file in prmtop_files:
        inpcrd_file = [inpcrd_file for inpcrd_file in inpcrd_files if inpcrd_file[:-7] == prmtop_file[:-7]][0]
        complex_file = [file for file in pdb_files if file[:-4] == prmtop_file[:-7]][0]

        first, last = get_protein_range(complex_file)

        create_dir(path=prmtop_file[:69], name='amber')
        output_path = f'{prmtop_file[:69]}amber/'
        prmtop_icm = f'{externals.ICM_PATH}/{prmtop_file[64:]}'
        inpcrd_icm = f'{externals.ICM_PATH}/{inpcrd_file[64:]}'
        complex_name = prmtop_file[64:68] if prmtop_file[64:68] not in externals.ab else prmtop_file[69:75]

        create_bash_file(output_filename=f'{output_path}{complex_name}_min-500',
                         content=[
                             '# Minimization performed for relaxing the solute : restraint_wt=500',
                             '&cntrl', 'imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,',
                             'ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,' 'ntf=1, ntb=1, dielc=1.0, cut=10.0,',
                             'nsnb=25, igb=0,',
                             f"ntr=1, restraint_wt=500, restraintmask='(:{first}-{last} & !@H= & !@Na= & !@Cl=)',",
                             'maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=0.0001,', 'ntc=1,', '/'])

        create_bash_file(output_filename=f'{output_path}{complex_name}_min-100',
                         content=[
                             '# Minimization performed for relaxing the solute : restraint_wt=1',
                             '&cntrl', 'imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,',
                             'ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,' 'ntf=1, ntb=1, dielc=1.0, cut=10.0,',
                             'nsnb=25, igb=0,',
                             f"ntr=1, restraint_wt=100, restraintmask='(:{first}-{last} & !@H= & !@Na= & !@Cl=)',",
                             'maxcyc=1500, ntmin=1, ncyc=100, dx0=0.01, drms=0.0001,', 'ntc=1,', '/'])

        create_bash_file(output_filename=f'{output_path}{complex_name}_min-5',
                         content=[
                             '# Minimization performed for relaxing the solute : restraint_wt=1',
                             '&cntrl', 'imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,',
                             'ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,' 'ntf=1, ntb=1, dielc=1.0, cut=10.0,',
                             'nsnb=25, igb=0,',
                             f"ntr=1, restraint_wt=5, restraintmask='(:{first}-{last} & !@H= & !@Na= & !@Cl=)',",
                             'maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=5,', 'ntc=1,', '/'])

        create_bash_file(output_filename=f'{output_path}{complex_name}_min',
                         content=[
                             '# Minimization performed for relaxing the solute : restraint_wt=1',
                             '&cntrl', 'imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,',
                             'ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,' 'ntf=1, ntb=1, dielc=1.0, cut=10.0,',
                             'nsnb=25, igb=0,', "ntr=0,",
                             'maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=0.0001,', 'ntc=1,', '/'])

        create_bash_file(output_filename=f'{output_path}{complex_name}_heat',
                         content=[
                             '# NVT Heating with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
                             'imin=0, ntx=1, irest=0, ntrx=1, ntxo=1,',
                             'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
                             'ntc=2, ntf=2, ntb=1, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,',
                             f"ntr=1, restraint_wt=50.0, restraintmask=':{first}-{last} & !@H= & !@Na= & !@Cl=',",
                             'nstlim=25000,', 't=0.0, dt=0.002,',
                             'ntt=3, gamma_ln=1.0, tempi=10.0, temp0=300.0,',
                             'vlimit=15,', 'ntp=0,', 'tol=0.00000001,', '/'])

        create_bash_file(output_filename=f'{output_path}{complex_name}-equil-NPT-50',
                         content=[
                             '# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
                             'imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,',
                             'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
                             'ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,',
                             f"ntr=1, restraint_wt=50.0, restraintmask=':{first}-{last} & !@H= & !@Na= & !@Cl=',",
                             'nstlim=10000,',
                             't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,', 'vlimit=15,',
                             'ntp=1, taup=1.0, pres0=1.0, comp=44.6,', 'tol=0.00000001, ', '/'])

        create_bash_file(output_filename=f'{output_path}{complex_name}-equil-NPT-10',
                         content=[
                             '# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
                             'imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,',
                             'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
                             'ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,',
                             f"ntr=1, restraint_wt=10.0, restraintmask=':{first}-{last} & !@H= & !@Na= & !@Cl=',",
                             'nstlim=10000,',
                             't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,', 'vlimit=15,',
                             'ntp=1, taup=1.0, pres0=1.0, comp=44.6,', 'tol=0.00000001, ', '/'])

        create_bash_file(output_filename=f'{output_path}{complex_name}-equil-NPT-2',
                         content=[
                             '# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
                             'imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,',
                             'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
                             'ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,',
                             f"ntr=1, restraint_wt=2.0, restraintmask=':{first}-{last} & !@H= & !@Na= & !@Cl=',",
                             'nstlim=10000,',
                             't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,', 'vlimit=15,',
                             'ntp=1, taup=1.0, pres0=1.0, comp=44.6,', 'tol=0.00000001, ', '/'])

        create_bash_file(output_filename=f'{output_path}{complex_name}-equil-NPT',
                         content=[
                             '# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
                             'imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,',
                             'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
                             'ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,', 'nstlim=10000,',
                             't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,', 'vlimit=15,',
                             'ntp=1, taup=1.0, pres0=1.0, comp=44.6,', 'tol=0.00000001, ', '/'])

        create_batch_file(batch_filename=f'{output_path}{complex_name}-amber.batch',
                          job_name=f'{complex_name}-amber',
                          slurm_out=f'{complex_name}-amber_slurm.out',
                          command=
                          f'srun sander.MPI -O -i {complex_name}_min-500 -p {prmtop_icm} -c {inpcrd_icm} '
                          f'-ref {inpcrd_icm} -o {complex_name}-min-500.ou -r '
                          f'{complex_name}-min-500.crd -inf {complex_name}-min-500.log\n'
                          
                          f'srun sander.MPI -O -i {complex_name}_min-100 -p {prmtop_icm} -c '
                          f'{complex_name}-min-500.crd -ref {complex_name}-min-500.crd -o {complex_name}-min-100.ou -r '
                          f'{complex_name}-min-100.crd -inf {complex_name}-min-100.log\n'
                          
                          f'srun sander.MPI -O -i {complex_name}_min-5 -p {prmtop_icm} -c '
                          f'{complex_name}-min-100.crd -ref {complex_name}-min-100.crd -o {complex_name}-min-5.ou -r '
                          f'{complex_name}-min-5.crd -inf {complex_name}-min-5.log\n'
                          
                          f'srun sander.MPI -O -i {complex_name}_min -p {prmtop_icm} -c '
                          f'{complex_name}-min-5.crd -ref {complex_name}-min-5.crd -o {complex_name}-min.ou -r '
                          f'{complex_name}-min.crd -inf {complex_name}-min.log\n'
                          
                          f'srun sander.MPI -O -i {complex_name}_heat -p {prmtop_icm} -c '
                          f'{complex_name}-min.crd -ref {complex_name}-min.crd -o {complex_name}-heat.ou -r '
                          f'{complex_name}-heat.crd -inf {complex_name}-heat.log\n'
                          
                          f'srun sander.MPI -O -i {complex_name}-equil-NPT-50 -p {prmtop_icm} -c '
                          f'{complex_name}-heat.crd -ref {complex_name}-heat.crd -o {complex_name}-equil-NPT-50.ou -r '
                          f'{complex_name}-equil-NPT-50.crd -inf {complex_name}-equil-NPT-50.log\n'
                          
                          f'srun sander.MPI -O -i {complex_name}-equil-NPT-10 -p {prmtop_icm} -c '
                          f'{complex_name}-equil-NPT-50.crd -ref {complex_name}-equil-NPT-50.crd -o '
                          f'{complex_name}-equil-NPT-10.ou -r {complex_name}-equil-NPT-10.crd -inf '
                          f'{complex_name}-equil-NPT-10.log\n'
                          
                          f'srun sander.MPI -O -i {complex_name}-equil-NPT-2 -p {prmtop_icm} -c '
                          f'{complex_name}-equil-NPT-10.crd -ref {complex_name}-equil-NPT-10.crd -o '
                          f'{complex_name}-equil-NPT-2.ou -r {complex_name}-equil-NPT-2.crd -inf '
                          f'{complex_name}-equil-NPT-2.log\n'
                         
                          f'srun sander.MPI -O -i {complex_name}-equil-NPT -p {prmtop_icm} -c '
                          f'{complex_name}-equil-NPT-2.crd -ref {complex_name}-equil-NPT-2.crd -o '
                          f'{complex_name}-equil-NPT.ou -r {complex_name}-equil-NPT.crd -inf '
                          f'{complex_name}-equil-NPT.log')


run()
