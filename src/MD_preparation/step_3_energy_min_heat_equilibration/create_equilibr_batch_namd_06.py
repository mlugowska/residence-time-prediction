from src.MD_preparation.step_3_energy_min_heat_equilibration.create_heat_batch_namd_04 import create
from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_batch_file(batch_filename: str, job_name: str, slurm_out: str, input_file: str, output_file: str) -> None:
    with open(batch_filename, "w") as f:
        lines = [
            '#!/bin/bash -l', f'#SBATCH -J {job_name}', '#SBATCH -N 1', '#SBATCH --ntasks-per-node 12',
            '#SBATCH --mem 5000', '#SBATCH --time=200:00:00', '#SBATCH --account=GR80-32',
            '#SBATCH --partition=topola', f'#SBATCH --output="{slurm_out}"',

            'module load apps/namd/2.13',
            f'mpirun namd2 {input_file} > {output_file}'
        ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def run_namd() -> None:
    equilibr_files = get_files(externals.COMPLEX_PATH, 'amber2namd_equilibr.in')

    for in_file in equilibr_files:
        create(in_file)


run_namd()
