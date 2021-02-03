from typing import Tuple, List

from src.utils import externals
from src.utils.get_pdb_files import get_files
from src.MD_preparation.step_3_energy_min_heat_equilibration.create_bash_file_amber_01 import create_dir, change_path


def create_heat_in_file(output_filename: str, prmtop_file: str, crd_file: str, output_path: str,
                        cell_vector_1: str, cell_vector_2: str, cell_vector_3: str, idx: int) -> None:
    with open(output_filename, "w") as f:
        lines = ['# AMBER parameters- force field and input coordinates', f'parmfile {prmtop_file}',
                 f'ambercoor {crd_file}', 'set temperature  300', 'temperature $temperature', '# output',
                 f'outputName {output_path[idx:]}_heat', 'binaryOutput yes',

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


def get_pdb_id_from_crd_file(crd_file: str) -> Tuple[int, int, int, str]:
    ab_conformations = ['6EYA', '5UGS', '5LNZ', '6DJ1', '2YKJ', '5J2X']
    if crd_file[66:70] in ab_conformations:
        pdb_idx = -23
        prmtop_file_idx = -27
        idx = -9
        complex_id = crd_file[pdb_idx:-14]
    else:
        pdb_idx = -22
        prmtop_file_idx = -26
        idx = -8
        complex_id = crd_file[pdb_idx:-14]
    return pdb_idx, prmtop_file_idx, idx, complex_id


def output_name(output_path: str, op_type='out'):
    if op_type == 'heat':
        return f'{output_path}_amber2namd_heating.in'
    if op_type == 'equil':
        return f'{output_path}_amber2namd_equilibr.in'
    return f'{output_path}_RAMD.sh'


def parse_crd_file(crd_file: str, prmtop_files: List[str], pdb_id_idx: int, dir_name: str, op_type: str,
                   complex_id=None, pdb=False, pdbs_after_equil=None, coor_files=None, xsc_files=None, vel_files=None) \
        -> Tuple[str, str, str, str, str, str, str]:
    output_path = f'{crd_file[:71]}{dir_name}/{crd_file[pdb_id_idx:-14]}'
    output_filename = output_name(output_path, op_type=op_type)

    prmtop_file = [prmtop_file for prmtop_file in prmtop_files if
                   prmtop_file[:-17] == f'{crd_file[:71]}{crd_file[pdb_id_idx:-14]}'][0]

    if pdb:
        pdb_file = [pdb_file for pdb_file in pdbs_after_equil if complex_id in pdb_file][0]
        coor_file = [pdb_file for pdb_file in coor_files if complex_id in pdb_file][0]
        xsc_file = [pdb_file for pdb_file in xsc_files if complex_id in pdb_file][0]
        vel_file = [pdb_file for pdb_file in vel_files if complex_id in pdb_file][0]
        return output_path, output_filename, prmtop_file, pdb_file, coor_file, xsc_file, vel_file

    return output_path, output_filename, prmtop_file, '', '', '', ''


def run() -> None:
    prmtop_files = get_files(externals.COMPLEX_PATH, 'prmtop')
    crd_files = get_files(externals.COMPLEX_PATH, 'equil-NPT.crd')

    for crd_file in crd_files:
        pdb_id_idx, prmtop_file_idx, idx, _ = get_pdb_id_from_crd_file(crd_file)
        create_dir(path=crd_file[:71], name='namd')
        output_path, output_filename, prmtop_file, _, _, _, _ = parse_crd_file(crd_file, prmtop_files, pdb_id_idx,
                                                                               dir_name='namd', op_type='heat')
        cell_vector_1, cell_vector_2, cell_vector_3 = get_cell_vectors_params(crd_file)
        create_heat_in_file(output_filename=output_filename, prmtop_file=prmtop_file, crd_file=crd_file,
                            cell_vector_1=cell_vector_1, cell_vector_2=cell_vector_2, cell_vector_3=cell_vector_3,
                            output_path=output_path, idx=idx)

        change_path(output_filename)


run()
