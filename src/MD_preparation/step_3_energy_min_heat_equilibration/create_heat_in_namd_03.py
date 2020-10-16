from typing import Tuple, List

from src.utils import externals
from src.utils.get_pdb_files import get_files
from src.MD_preparation.step_3_energy_min_heat_equilibration.create_bash_file_amber_01 import create_dir


def create_heat_in_file(output_filename: str, prmtop_file: str, crd_file: str, output_path: str,
                        cell_vector_1: str, cell_vector_2: str, cell_vector_3: str, idx: int) -> None:
    with open(output_filename, "w") as f:
        lines = ['# AMBER parameters- force field and input coordinates', f'parmfile {prmtop_file}',
                 f'ambercoor {crd_file}', 'set temperature  300', 'temperature $temperature', '# output',
                 f'outputName {output_path[idx:]}_heat', 'binaryOutput no',

                 '# initial temperature/velocities',
                 '# dcd output', f'dcdFile {output_path}_heat.dcd', 'dcdFreq 5000',
                 f'velDcdFile {output_path}_heat.vel.dcd', 'velDcdFreq 5000',

                 '# forcefield parameters modified for AMBER', 'amber yes', 'readexclusions     yes',
                 'exclude            scaled1-4', '1-4scaling         0.83333333   #=1/1.2', 'scnb               2',
                 'parameters .prmtop',

                 '# forcefield parameters', '# cutoffs', 'switching on', 'switchDist 8.0', 'cutoff 10.0',
                 'pairListDist 11',

                 '# Integrator Parameters', 'timestep            2.0          ;# 2fs/step',
                 'rigidBonds          all          ;# needed for 2fs steps', 'rigidTolerance     1e-08',
                 'nonbondedFreq       1', 'fullElectFrequency  2', 'pairlistsPerCycle   2', 'stepspercycle       20',
                 'twoawayx            yes',

                 '# Constant Temperature Control', 'langevin            on            ;# langevin dynamics',
                 'langevinDamping     3.0            ;# damping coefficient of 5/ps, 1/ps is enough for MD',
                 '##langevinTemp        $temperature  ;# random noise at this level',
                 'langevinHydrogen    no            ;# dont couple bath to hydrogens',

                 f'cellBasisVector1    {cell_vector_1}     0.   0.',
                 f'cellBasisVector2    0    {cell_vector_2}     0. ',
                 f'cellBasisVector3    0                  0      {cell_vector_3}',

                 'wrapAll             off', 'wrapWater           off', 'PME                 yes',
                 'PMETolerance       1e-06', 'PMEGridSpacing       1',

                 'ldbUnloadOne      yes', 'noPatchesOnOne      yes',

                 '# Nose-Hoover Langevin piston method ', '##langevinPiston        on',
                 '##langevinPistonTarget  1.01325      ;# pressure in bar -> 1 atm',
                 '##langevinPistonPeriod  1000.         ;# oscillation period around 100 fs',
                 '##langevinPistonDecay   1000.          ;# oscillation decay time of 50 fs',
                 '##langevinPistonTemp    $temperature ;# coupled to heat bath',

                 '# Constant Pressure Control (variable volume)',
                 '##useGroupPressure      yes ;# needed for rigid bonds',
                 '##useFlexibleCell       no  ;# no for water box, yes for membrane',
                 '##useConstantArea       no  ;# no for water box, maybe for membrane',

                 f'restartname {output_path[idx:]}_heat', 'restartfreq 10000', 'binaryrestart yes',
                 'firsttimestep      0      # reset frame counter',

                 '#=========== constant pressure heating (by changing velocity) ',
                 'for {set i 10} {$i < $temperature} {incr i 10} {', '  set tempr $i', '  langevinTemp $tempr',
                 '  reinitvels   $tempr', '  run 10000', '}'
                 ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def get_cell_vectors_params(crd_file: str) -> Tuple[str, str, str]:
    with open(crd_file, 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        return last_line[2:12], last_line[14:24], last_line[26:36]


def change_path(heat_in_file: str) -> None:
    file_in = open(heat_in_file, 'rt')
    data = file_in.read()
    data = data.replace(externals.COMPLEX_PATH, externals.COMPLEX_ICM_PATH)
    file_in.close()
    file_out = open(heat_in_file, 'wt')
    file_out.write(data)


def get_pdb_id_from_crd_file(crd_file: str) -> Tuple[int, int, int]:
    ab_conformations = ['6EYA', '5UGS', '5LNZ', '6DJ1', '2YKJ', '5J2X']

    if crd_file[66:70] in ab_conformations:
        return -23, -27, -9
    return -22, -26, -8


def parse_crd_file(crd_file: str, prmtop_files: List[str], pdb_id_idx: int, heat=False) -> Tuple[str, str, str]:
    output_path = f'{crd_file[:71]}namd/{crd_file[pdb_id_idx:-14]}'
    output_filename = f'{output_path}_amber2namd_heating.in' if heat else f'{output_path}_amber2namd_equilibr.in'
    prmtop_file = [prmtop_file for prmtop_file in prmtop_files if
                   prmtop_file[:-17] == f'{crd_file[:71]}{crd_file[pdb_id_idx:-14]}'][0]

    return output_path, output_filename, prmtop_file


def run() -> None:
    prmtop_files = get_files(externals.COMPLEX_PATH, 'prmtop')
    crd_files = get_files(externals.COMPLEX_PATH, 'equil-NPT.crd')

    for crd_file in crd_files:
        pdb_id_idx, prmtop_file_idx, idx = get_pdb_id_from_crd_file(crd_file)
        output_path, output_filename, prmtop_file = parse_crd_file(crd_file, prmtop_files, pdb_id_idx, heat=True)
        create_dir(path=prmtop_file[:prmtop_file_idx], name='namd')
        cell_vector_1, cell_vector_2, cell_vector_3 = get_cell_vectors_params(crd_file)
        create_heat_in_file(output_filename=output_filename, prmtop_file=prmtop_file, crd_file=crd_file,
                            cell_vector_1=cell_vector_1, cell_vector_2=cell_vector_2, cell_vector_3=cell_vector_3,
                            output_path=output_path, idx=idx)

        change_path(output_filename)


run()
