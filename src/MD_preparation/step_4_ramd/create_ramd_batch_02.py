from src.MD_preparation.step_3_energy_min_heat_equilibration.create_heat_batch_namd_04 import create
from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_batch_file(batch_filename: str, job_name: str, slurm_out: str, input_file: str, output_file: str, i: str) \
        -> None:
    with open(batch_filename, "w") as f:
        lines = [
            '#!/bin/bash -l', f'#SBATCH -J {job_name}', '#SBATCH --nodes=2', '#SBATCH --ntasks-per-node=14',
            '#SBATCH --cpus-per-task=2', '#SBATCH --account=GR80-32',
            '#SBATCH --partition=topola', f'#SBATCH --output="{slurm_out}"',

            'module load apps/namd/2.13',
            f'sh {input_file} {i}'
        ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def run_namd() -> None:
    ramd_files = get_files(externals.COMPLEX_PATH, 'RAMD.sh')

    for in_file in ramd_files:
        for i in range(101, 111):
            create(in_file, create_batch_file, i)


run_namd()
