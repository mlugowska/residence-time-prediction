from subprocess import call


def determine_bond_and_atom_types(ligand_mol2: str, output_filename: str) -> None:
    '''
    Determine the bond and atom types of the ligand
    '''

    cmd = ['parmchk2', '-i', f'{ligand_mol2}', '-f', 'mol2', '-o', f'{output_filename}']
    call(cmd)
