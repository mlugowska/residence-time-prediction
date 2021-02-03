from src.MD_preparation.step_3_energy_min_heat_equilibration.create_heat_in_namd_03 import get_pdb_id_from_crd_file, \
    parse_crd_file, change_path
from src.utils import externals
from src.utils.get_pdb_files import get_files
from src.MD_preparation.step_3_energy_min_heat_equilibration.create_bash_file_amber_01 import create_dir


def create_ramd_file(output_filename: str, prot_last_atom: int, lig_first_atom: int, lig_last_atom: int,
                     path: str, prmtop_file: str, crd_file: str, coor_file: str, vel_file: str,
                     xsc_file: str, complex_id: str) -> None:
    with open(output_filename, "w") as f:
        lines = [f'maxprot={prot_last_atom}', f'minlig={lig_first_atom}', f'maxlig={lig_last_atom}',
                 f'molname={complex_id}', 'force=16', f'path={path}',

                 f'topfile={prmtop_file}', f'rstfile={crd_file}', f'bincoor={coor_file}', f'binvel={vel_file}',
                 f'xscfile={xsc_file}',

                 'number=$1',

                 'outdir=${molname}_${number}_ramd_force_${force}_out',

                 'if [ -d "$outdir" ]; then rm -rf $outdir; mkdir $outdir; else mkdir $outdir; fi',

                 'cat << EOF > ${path}/${molname}_${number}_ramd_force_${force}_rMin_025.namdin',

                 '# *** AMBER force field ********************************************************',
                 'amber                                         on',
                 'parmfile                                   $topfile',
                 'ambercoor                                  $rstfile',
                 'bincoordinates                             $bincoor',
                 'readexclusions                               yes', 'exclude                                scaled1-4',
                 '1-4scaling                                     0.83333333   #=1/1.2',
                 'scnb                                           2',

                 '#*** approximations for nonbonded interactions***********************************',
                 'cutoff                                        10',
                 'switching                                     on',
                 'switchdist                                    8.0',
                 'pairlistdist                                  11',
                 'outputpairlists                             1000',
                 'stepspercycle                                 20',
                 'nonbondedfreq                                  1',
                 'fullelectfrequency                             2',
                 'pairlistsPerCycle   2', 'twoawayx            yes', 'ldbUnloadOne      yes', 'noPatchesOnOne      yes',

                 '# ***timestep*********************************************************************',
                 'minimization                                 off',
                 'numsteps                                    1000000',
                 'timestep                                       2',
                 '# ***SHAKE use', 'rigidbonds                                   all',
                 'rigidTolerance                             1e-08',

                 '# ***Basic Dynamics***************************************************************',
                 'zeroMomentum                                  no',

                 '#***temperature control**********************************************************',
                 'binvelocities                            $binvel', 'langevin                                      on',
                 'langevintemp                                 300.0',
                 'langevindamping                                1.0',
                 'langevinhydrogen                             off',

                 '# ***initial contraints***********************************************************',
                 'constraints                                  off',

                 '# ***pressure control*************************************************************',
                 'useGroupPressure                             yes',
                 'useFlexibleCell                               no',
                 'useConstantArea                               no',
                 'LangevinPiston                                on',
                 'LangevinPistonTarget                           1.01325',
                 'LangevinPistonPeriod                        1000',
                 'LangevinPistonDecay                         1000',
                 'LangevinPistonTemp                           300',
                 '# SurfaceTensionTarget                          60',

                 '# ***PME and PBC******************************************************************',
                 'PME                                      on', 'PMETolerance                               1e-06',
                 'PMEGridSpacing                                 1',
                 'extendedSystem                             $xscfile',
                 'wrapAll                                      off',
                 'XSTfile                               ${outdir}/${molname}_eq04_${number}_ramd_1.xst',
                 'XSTfreq                                     1000',

                 '# ***Interactive Molecular Dynamics***********************************************',
                 'IMDon                                        off',

                 '#***output***********************************************************************',
                 'outputname                             ${outdir}/${molname}_${number}_ramd_0${force}',
                 'outputenergies                              500 ',
                 'outputtiming                                1000 ',
                 'restartname                            ${outdir}/${molname}_${number}_ramd_0${force}.rst',
                 'restartfreq                                 2000',
                 'dcdfile                                ${outdir}/${molname}_${number}_ramd_0${force}.dcd',
                 'dcdfreq                                     500',
                 'veldcdfile                            ${outdir}/${molname}_${number}_ramd_0${force}.vcd',
                 'veldcdfreq                                  2000', 'binaryoutput                                 off',
                 'binaryrestart                                 on',

                 '# *** Random Acceleration Molecular Dynamics *************************************',
                 'source /lu/topola/temp/mszpindl/namd-2.13/lib/ramd-4.1/scripts/ramd-4.1.tcl',
                 '# *** sources the wrapper script out-4.1.tcl;',
                 "# *** please change the directory '../scripts/' to '$dir' ( the correct path );",
                 "# *** directory '$dir' should contain the scripts: out-4.1.tcl, out-4.1_script.tcl, and vectors.tcl",

                 'ramd debugLevel                       0',
                 '# *** activates verbose output if set to something else than 0',

                 'ramd ramdSteps                       50', '# *** specifies the number of steps in 1 out stint; ',
                 '# *** defaults to 50',

                 '#ramd forceRAMD                          ${force}', '# *** specifies the acceleration to be applied; ',
                 '# *** defaults to 0.25 kcal/mol*A*amu',

                 'ramd rMinRamd                         0.025',
                 '# *** specifies the minimum distance to be travelled by the ligand in 1 out stint; ',
                 '# *** defaults to 0.01 Angstr',

                 'ramd forceOutFreq                    10',
                 "# *** every 'forceOutFreq' steps detailed output of forces will be written; ",
                 '# *** defaults to 0 (no detailed output)',

                 'ramd maxDist                        40',
                 '# *** specifies the distance between the COMs of the ligand and the protein '
                 'when the simulation is stopped',
                 '# *** defaults to 50 Angstr',

                 'ramd firstProtAtom                    1', '# *** specifies the index of the first protein atom',
                 '# *** defaults to 1 (assumes first atom in the system corresponds to first protein atom',

                 'ramd lastProtAtom                  ${maxprot}', '# *** specifies the index of the last protein atom',
                 '# *** required; simulation exits if this parameter is not set',

                 'ramd firstRamdAtom                 ${minlig}', '# *** specifies the index of the first ligand atom',
                 '# *** required; simulation exits if this parameter is not set',

                 'ramd lastRamdAtom                  ${maxlig}', '# *** specifies the index of the last ligand atom',
                 '# *** required; simulation exits if this parameter is not set',

                 'ramd ramdSeed                     ${number}',
                 '# *** specifies the seed for the random number generator '
                 '(for the generation of acceleration directions)',
                 '# *** defaults to 14253 ', '# *** please change if you wish to run different trajectories', 'EOF',

                 '####################################################################################',
                 'srun namd2 ++ppn 2 ${path}/${molname}_${number}_ramd_force_${force}_rMin_025.namdin > '
                 '${outdir}/${molname}_${number}_ramd_force_${force}_rMin_025.out  #cm-launcher',
                 'exit',
                 ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def get_atom_numbers(pdb_file: str, complex_id: str):
    import tempfile
    ligand_name = complex_id[-3:]
    tmp = tempfile.NamedTemporaryFile()

    with open(tmp.name, 'w') as temp:
        with open(pdb_file, "r") as f:
            lines = f.readlines()
            previous_line = ''
            for line in lines:
                if ligand_name in line:
                    if ligand_name not in previous_line:
                        prot_last_atom = int(previous_line[6:11])
                    temp.write(line)
                previous_line = line

    with open(tmp.name) as temp:
        first = temp.readline()
        for last in temp:
            pass
    return int(first[6:11]), int(last[6:11]), prot_last_atom


def run() -> None:
    prmtop_files = get_files(externals.COMPLEX_PATH, 'prmtop')
    crd_files = get_files(externals.COMPLEX_PATH, 'equil-NPT.crd')
    pdbs_after_equil = get_files(externals.COMPLEX_PATH, 'equilibr-first.pdb')
    coor_files = get_files(externals.COMPLEX_PATH, 'equilibr.coor')
    xsc_files = get_files(externals.COMPLEX_PATH, 'equilibr.xsc')
    vel_files = get_files(externals.COMPLEX_PATH, 'equilibr.vel')

    for crd_file in crd_files:
        try:
            pdb_id_idx, prmtop_file_idx, idx, complex_id = get_pdb_id_from_crd_file(crd_file)
            output_path, output_filename, prmtop_file, pdb_file, coor_file, xsc_file, vel_file = \
                parse_crd_file(crd_file=crd_file, prmtop_files=prmtop_files, pdb_id_idx=pdb_id_idx,
                               pdbs_after_equil=pdbs_after_equil, dir_name='ramd', op_type='ramd', pdb=True,
                               complex_id=complex_id, coor_files=coor_files, vel_files=vel_files, xsc_files=xsc_files)
            if pdb_file:
                create_dir(path=crd_file[:71], name='ramd')
                lig_first_atom, lig_last_atom, prot_last_atom = get_atom_numbers(pdb_file, complex_id)
                create_ramd_file(path=output_path[:75], complex_id=complex_id, lig_first_atom=lig_first_atom, lig_last_atom=lig_last_atom,
                                 prot_last_atom=prot_last_atom, output_filename=output_filename, prmtop_file=prmtop_file,
                                 crd_file=crd_file, coor_file=coor_file, xsc_file=xsc_file, vel_file=vel_file)
                change_path(output_filename)
        except IndexError:
            print(f'{crd_file[-23:-14]} Equilibration in progress - pdb file not ready')


run()
