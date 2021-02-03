from subprocess import call

from src.utils import externals
from src.utils.get_pdb_files import get_files


def call_file(bash_file: str) -> None:
    cmd = ['sh', f'{bash_file}']
    call(cmd)


def run_amber() -> None:
    bash_files = get_files(externals.COMPLEX_PATH, 'amber_prep.sh')

    for bash_file in bash_files:
        print(f'Run complex id: {bash_file[71:75]}')
        call_file(bash_file)


run_amber()
