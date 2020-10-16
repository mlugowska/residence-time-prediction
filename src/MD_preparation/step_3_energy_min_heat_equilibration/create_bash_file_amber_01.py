import os
from typing import Tuple

from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_bash_file(output_filename: str, pdb_id: str, complex_prmtop: str, complex_inpcrd: str, path: str,
                     first: int, last: int) -> None:
    with open(output_filename, "w") as f:
        lines = [
            '#!/bin/bash',
            'echo "', '# Minimization performed for relaxing the solute : restraint_wt=500',
            '&cntrl', 'imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,',
            'ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,' 'ntf=1, ntb=1, dielc=1.0, cut=10.0,',
            'nsnb=25, igb=0,', f"ntr=1, restraint_wt=500, restraintmask='(:{first}-{last} & !@H= & !@Na= & !@Cl=)',",
            'maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=0.0001,', 'ntc=1,', '/', f'" >> {path}{pdb_id}_min-500',
            f'sander -O -i {path}{pdb_id}_min-500 -p {complex_prmtop} -c {complex_inpcrd} -ref {complex_inpcrd} -o '
            f'{path}{pdb_id}-min-500.ou -r {path}{pdb_id}-min-500.crd -inf {path}{pdb_id}-min-500.log',

            'echo "', '# Minimization performed for relaxing the solute : restraint_wt=1',
            '&cntrl', 'imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,',
            'ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,' 'ntf=1, ntb=1, dielc=1.0, cut=10.0,',
            'nsnb=25, igb=0,', f"ntr=1, restraint_wt=100, restraintmask='(:{first}-{last} & !@H= & !@Na= & !@Cl=)',",
            'maxcyc=1500, ntmin=1, ncyc=100, dx0=0.01, drms=0.0001,', 'ntc=1,', '/', f'" >> {path}{pdb_id}_min-100',
            f'sander -O -i {path}{pdb_id}_min-100 -p {complex_prmtop} -c {path}{pdb_id}-min-500.crd -ref {path}{pdb_id}-min-500.crd -o '
            f'{path}{pdb_id}-min-100.ou -r {path}{pdb_id}-min-100.crd -inf {path}{pdb_id}-min-100.log',

            'echo "', '# Minimization performed for relaxing the solute : restraint_wt=1',
            '&cntrl', 'imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,',
            'ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,' 'ntf=1, ntb=1, dielc=1.0, cut=10.0,',
            'nsnb=25, igb=0,', f"ntr=1, restraint_wt=5, restraintmask='(:{first}-{last} & !@H= & !@Na= & !@Cl=)',",
            'maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=5,', 'ntc=1,', '/', f'" >> {path}{pdb_id}_min-5',
            f'sander -O -i {path}{pdb_id}_min-5 -p {complex_prmtop} -c {path}{pdb_id}-min-100.crd -ref {path}{pdb_id}-min-100.crd -o '
            f'{path}{pdb_id}-min-5.ou -r {path}{pdb_id}-min-5.crd -inf {path}{pdb_id}-min-5.log',

            'echo "', '# Minimization performed for relaxing the solute : restraint_wt=1',
            '&cntrl', 'imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,',
            'ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,' 'ntf=1, ntb=1, dielc=1.0, cut=10.0,',
            'nsnb=25, igb=0,', "ntr=0,",
            'maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=0.0001,', 'ntc=1,', '/', f'" >> {path}{pdb_id}_min',
            f'sander -O -i {path}{pdb_id}_min -p {complex_prmtop} -c {path}{pdb_id}-min-5.crd -ref {path}{pdb_id}-min-5.crd -o '
            f'{path}{pdb_id}-min.ou -r {path}{pdb_id}-min.crd -inf {path}{pdb_id}-min.log',

            'echo "', '# NVT Heating with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
            'imin=0, ntx=1, irest=0, ntrx=1, ntxo=1,', 'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
            'ntc=2, ntf=2, ntb=1, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,',
            f"ntr=1, restraint_wt=50.0, restraintmask=':{first}-{last} & !@H= & !@Na= & !@Cl=',", 'nstlim=25000,',
            't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=10.0, temp0=300.0,', 'vlimit=15,', 'ntp=0,',
            'tol=0.00000001,', " /'", f'" >> {path}{pdb_id}_heat',
            f'sander -O -i {path}{pdb_id}_heat -p {complex_prmtop} -c {path}{pdb_id}-min.crd -ref {path}{pdb_id}-min.crd -o '
            f'{path}{pdb_id}-heat.ou -r {path}{pdb_id}-heat.crd -inf {path}{pdb_id}-heat.log',

            'echo "', '# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
            'imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,', 'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
            'ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,',
            f"ntr=1, restraint_wt=50.0, restraintmask=':{first}-{last} & !@H= & !@Na= & !@Cl=',", 'nstlim=10000,',
            't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,', 'vlimit=15,',
            'ntp=1, taup=1.0, pres0=1.0, comp=44.6,', 'tol=0.00000001, ', '/', f'" >> {path}{pdb_id}-equil-NPT-50',
            f'sander -O -i {path}{pdb_id}-equil-NPT-50 -p {complex_prmtop} -c {path}{pdb_id}-heat.crd -ref {path}{pdb_id}-heat.crd -o '
            f'{path}{pdb_id}-equil-NPT-50.ou -r {path}{pdb_id}-equil-NPT-50.crd -inf {path}{pdb_id}-equil-NPT-50.log -x '
            f'{path}{pdb_id}-equil-NPT-50.mdcrd',

            'echo "', '# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
            'imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,', 'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
            'ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,',
            f"ntr=1, restraint_wt=10.0, restraintmask=':{first}-{last} & !@H= & !@Na= & !@Cl=',", 'nstlim=10000,',
            't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,', 'vlimit=15,',
            'ntp=1, taup=1.0, pres0=1.0, comp=44.6,', 'tol=0.00000001, ', '/', f'" >> {path}{pdb_id}-equil-NPT-10',
            f'sander -O -i {path}{pdb_id}-equil-NPT-10 -p {complex_prmtop} -c {path}{pdb_id}-equil-NPT-50.crd -ref '
            f'{path}{pdb_id}-equil-NPT-50.crd -o {path}{pdb_id}-equil-NPT-10.ou -r {path}{pdb_id}-equil-NPT-10.crd -inf '
            f'{path}{pdb_id}-equil-NPT-10.log -x {path}{pdb_id}-equil-NPT-10.mdcrd',

            'echo "', '# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
            'imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,', 'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
            'ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,',
            f"ntr=1, restraint_wt=2.0, restraintmask=':{first}-{last} & !@H= & !@Na= & !@Cl=',", 'nstlim=10000,',
            't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,', 'vlimit=15,',
            'ntp=1, taup=1.0, pres0=1.0, comp=44.6,', 'tol=0.00000001, ', '/', f'" >> {path}{pdb_id}-equil-NPT-2',
            f'sander -O -i {path}{pdb_id}-equil-NPT-2 -p {complex_prmtop} -c {path}{pdb_id}-equil-NPT-10.crd -ref '
            f'{path}{pdb_id}-equil-NPT-10.crd -o {path}{pdb_id}-equil-NPT-2.ou -r {path}{pdb_id}-equil-NPT-2.crd -inf '
            f'{path}{pdb_id}-equil-NPT-2.log -x {path}{pdb_id}-equil-NPT-2.mdcrd',

            'echo "', '# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2', '&cntrl',
            'imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,', 'ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,',
            'ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,', 'nsnb=100, igb=0,', 'nstlim=10000,',
            't=0.0, dt=0.002,', 'ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,', 'vlimit=15,',
            'ntp=1, taup=1.0, pres0=1.0, comp=44.6,', 'tol=0.00000001, ', '/', f'" >> {path}{pdb_id}-equil-NPT',
            f'sander -O -i {path}{pdb_id}-equil-NPT -p {complex_prmtop} -c {path}{pdb_id}-equil-NPT-2.crd -ref '
            f'{path}{pdb_id}-equil-NPT-2.crd -o {path}{pdb_id}-equil-NPT.ou -r {path}{pdb_id}-equil-NPT.crd -inf '
            f'{path}{pdb_id}-equil-NPT.log -x {path}{pdb_id}-equil-NPT.mdcrd',
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
    prmtop_files = get_files(externals.COMPLEX_PATH, 'prmtop')
    inpcrd_files = get_files(externals.COMPLEX_PATH, 'inpcrd')
    pdb_files = get_files(externals.COMPLEX_PATH, 'tip3_ions.pdb')

    for prmtop_file in prmtop_files:
        inpcrd_file = [inpcrd_file for inpcrd_file in inpcrd_files if inpcrd_file[:-7] == prmtop_file[:-7]][0]
        complex_file = [file for file in pdb_files if file[:-4] == prmtop_file[:-7]][0]
        first, last = get_protein_range(complex_file)
        ab_conformations = ['6EYA', '5UGS', '5LNZ', '6DJ1', '2YKJ', '5J2X']
        output_filename = f'{prmtop_file[:-17]}_amber_prep.sh'

        create_dir(path=output_filename[:-23], name='amber')

        if prmtop_file[-26:-22] in ab_conformations:
            complex_name = prmtop_file[-26:-17]
            output_path = f'{output_filename[:-23]}amber/'
        else:
            complex_name = prmtop_file[-25:-17]
            output_path = f'{output_filename[:-22]}amber/'

        create_bash_file(output_filename=output_filename, complex_prmtop=prmtop_file, pdb_id=complex_name,
                         complex_inpcrd=inpcrd_file, path=output_path, first=first, last=last)


run()
