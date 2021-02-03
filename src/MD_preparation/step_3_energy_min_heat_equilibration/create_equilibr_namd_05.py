from src.MD_preparation.step_3_energy_min_heat_equilibration.create_heat_in_namd_03 import get_pdb_id_from_crd_file, \
    parse_crd_file, change_path
from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_equilibr_file(output_filename: str, prmtop_file: str, crd_file: str, output_path: str, idx: int) -> None:
    with open(output_filename, "w") as f:
        lines = ['# AMBER parameters- force field and input coordinates', f'parmfile {prmtop_file}',
                 f'ambercoor {crd_file}', 'set temperature  300',

                 f'bincoordinates {output_path[idx:]}_heat.coor', f'binvelocities  {output_path[idx:]}_heat.vel',
                 f'extendedSystem {output_path[idx:]}_heat.xsc', '# output', f'outputName {output_path[idx:]}_equilibr',
                 'binaryOutput yes',

                 '# initial temperature/velocities',
                 '# dcd output', f'dcdFile {output_path}_equilibr.dcd', 'dcdFreq 1000',
                 f'velDcdFile {output_path}_equilibr.vel.dcd', 'velDcdFreq 1000',

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
                 'langevinTemp        $temperature  ;# random noise at this level',
                 'langevinHydrogen    no            ;# dont couple bath to hydrogens',

                 'wrapAll             off', 'wrapWater           off', 'PME                 yes',
                 'PMETolerance       1e-06', 'PMEGridSpacing       1',

                 'ldbUnloadOne      yes', 'noPatchesOnOne      yes',

                 '# md', 'numSteps 10000000', f'restartname {output_path[idx:]}_equilibr', 'restartfreq 1000',
                 'binaryrestart yes', 'firsttimestep      0  # reset frame counter'

                                      '# Nose-Hoover Langevin piston method ', 'langevinPiston        on',
                 'langevinPistonTarget  1.01325      ;# pressure in bar -> 1 atm',
                 'langevinPistonPeriod  1000.         ;# oscillation period around 100 fs',
                 'langevinPistonDecay   1000.          ;# oscillation decay time of 50 fs',
                 'langevinPistonTemp    $temperature ;# coupled to heat bath',

                 '# Constant Pressure Control (variable volume)',
                 'useGroupPressure      yes ;# needed for rigid bonds',
                 'useFlexibleCell       no  ;# no for water box, yes for membrane',
                 'useConstantArea       no  ;# no for water box, maybe for membrane',
                 ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def run() -> None:
    prmtop_files = get_files(externals.COMPLEX_PATH, 'prmtop')
    crd_files = get_files(externals.COMPLEX_PATH, 'equil-NPT.crd')

    for crd_file in crd_files:
        pdb_id_idx, prmtop_file_idx, idx, _ = get_pdb_id_from_crd_file(crd_file)
        output_path, output_filename, prmtop_file, _, _, _, _ = parse_crd_file(crd_file, prmtop_files, pdb_id_idx,
                                                                               dir_name='namd', op_type='equil')
        create_equilibr_file(output_filename=output_filename, prmtop_file=prmtop_file, crd_file=crd_file,
                             output_path=output_path, idx=idx)
        change_path(output_filename)


run()
