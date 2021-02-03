import os

from src.utils import externals
from src.utils.get_pdb_files import get_files


def create_batch_file(batch_filename: str, job_name: str, slurm_out: str, input_file: str, output_file: str) -> None:
    with open(batch_filename, "w") as f:
        lines = [
            '#!/bin/bash -l', f'#SBATCH -J {job_name}', '#SBATCH --nodes=6', '#SBATCH --ntasks-per-node=10',
            '#SBATCH --cpus-per-task=2', '#SBATCH --account=GR80-32',
            '#SBATCH --partition=topola', f'#SBATCH --output="{slurm_out}"',

            'module load apps/namd/2.13',
            f'srun namd2 ++ppn 2 {input_file} > {output_file}'
        ]

        for line_ in lines:
            f.writelines(line_)
            f.writelines('\n')


def create(in_file: str, batch_file_func, i=None) -> None:
    path, file = os.path.split(in_file)
    batch_filename = f'{in_file[:-3]}_{i}.batch' if i else f'{in_file[:-3]}.batch'
    job_name = f'{file[:4]}_{i}' if i else f'{file[:-3]}'
    slurm_out = f'{file[:-3]}_{i}_slurm.out' if i else f'{file[:-3]}_slurm.out'
    out_file = f'{file[:-3]}_{i}.out' if i else f'{file[:-3]}.out'
    if i:
        batch_file_func(batch_filename=batch_filename, job_name=job_name, slurm_out=slurm_out, output_file=out_file,
                        input_file=file, i=i)
    else:
        batch_file_func(batch_filename=batch_filename, job_name=job_name, slurm_out=slurm_out, output_file=out_file,
                        input_file=file)


def run_namd() -> None:
    heat_in_files = get_files(externals.COMPLEX_PATH, 'amber2namd_heating.in')

    for in_file in heat_in_files:
        create(in_file, create_batch_file)


run_namd()
