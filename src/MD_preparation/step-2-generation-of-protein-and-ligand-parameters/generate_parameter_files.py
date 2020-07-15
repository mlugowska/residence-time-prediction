from subprocess import call


def determine_bond_and_atom_types(ligand_mol2, output_filename):
    cmd = ['parmchk', '-i', f'{ligand_mol2}', '-f', 'mol2', '-o', f'{output_filename}']
    call(cmd)


def generate_topology_coordinate_pdb_files(tleap_ligand_in):
    '''
    tleap_ligand_in: tleap input file for generation of the ligand parameters
    tleap_all_in: tleap input file for generation of the topology and coordinate files of the complex
    :return:
    '''
    cmd = ['tleap', '-f', f'{tleap_ligand_in}']
    call(cmd)


def combine_files(complex_file):
    '''
    Combine the protein, ligand, and crystallographic water PDB files into one file in which
    their coordinates are separated by TER lines:
    '''
    cmd_1 = ['grep', 'ATOM', f'{protein_file}', '>', f'{complex_file}']
    # grep ATOM protein.pdb > prot_lig.pdb
    cmd_2 = ['echo', 'TER', '>>', f'{complex_file}']
    # echo "TER" >> prot_lig.pdb
    cmd_3 = ['grep', f'{ligand_code}', f'{ligand_file_pdb}', '>>', f'{complex_file}']
    # grep INH INH.pdb >> prot_lig.pdb
    cmd_4 = ['echo', 'TER', '>>', f'{complex_file}']
    # echo "TER" >> prot_lig.pdb
    cmd_5 = ['grep', 'HOH', f'{water_file}', '>>', f'{complex_file}']
    # grep HOH  water2.pdb  >>  prot_lig.pdb


def solvate_system_add_ions():
    # tleap -f tleap_all_in which outputs topology (ref.prmtop), PDB (ref.pdb)  and coordinate (ref.impcrd) files in Amber format.
    pass
