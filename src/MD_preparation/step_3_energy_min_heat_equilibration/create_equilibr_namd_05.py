from src.MD_preparation.step_3_energy_min_heat_equilibration.create_heat_in_namd_03 import output_name
from src.utils import externals
from src.utils.get_pdb_files import get_files, get_md_files


def create_equilibr_file(output_filename: str, prmtop_file: str, crd_file: str, output_name: str) -> None:
    with open(output_filename, "w") as f:
        lines = ['# AMBER parameters- force field and input coordinates', f'parmfile {prmtop_file}',
                 f'ambercoor {crd_file}', 'set temperature  300',

                 f'bincoordinates {output_name}_heat.coor', f'binvelocities  {output_name}_heat.vel',
                 f'extendedSystem {output_name}_heat.xsc', '# output', f'outputName {output_name}_equilibr',
                 'binaryOutput yes',

                 '# initial temperature/velocities',
                 '# dcd output', f'dcdFile {output_name}_equilibr.dcd', 'dcdFreq 1000',
                 f'velDcdFile {output_name}_equilibr.vel.dcd', 'velDcdFreq 1000',

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

                 '# md', 'numSteps 10000000', f'restartname {output_name}_equilibr', 'restartfreq 1000',
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
    pdbs = list(externals.PDB_TO_DO.keys())
    prmtop_files = get_files(externals.DATA_PATH, 'ions.prmtop', given_dirs=pdbs)

    for pdb_id in pdbs:
        path = f'{externals.DATA_PATH}/{pdb_id}'

        crd_file = get_md_files(f'{path}/amber/', 'equil-NPT.crd')[0]

        prmtop_file = [file for file in prmtop_files if pdb_id in file][0]
        output_binary_filenames = f'{pdb_id}_{externals.PDB_TO_DO.get(pdb_id)}'
        output_file = f'{externals.DATA_PATH}/{pdb_id}/namd/configs/{output_binary_filenames}'
        output_filename = output_name(output_path=output_file, op_type='equil')

        icm_path = f'{externals.ICM_PATH}/{pdb_id}'

        icm_crd = f'{icm_path}{crd_file[len(path):]}'
        icm_prmtop = f'{icm_path}{prmtop_file[len(path):]}'

        create_equilibr_file(crd_file=icm_crd, prmtop_file=icm_prmtop, output_name=output_binary_filenames,
                             output_filename=output_filename)


run()
