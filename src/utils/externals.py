# PATHS
DATA_PATH = '/Users/magdalena/PycharmProjects/residence-time-prediction/data'
OUTPUT_PATH = \
    '/Users/mlugowska/PycharmProjects/residence-time-prediction/src/feature_generation/protein_ligand_interactions/binana/output'
BINANA_PATH = '/Users/mlugowska/PycharmProjects/tools/binana/binana.py'
BINANA_INTERACTIONS_PATH = \
    '/Users/mlugowska/PycharmProjects/residence-time-prediction/src/feature_generation/protein_ligand_interactions'
STRUCTURES_FILE = '/Users/mlugowska/PycharmProjects/residence_time/PDBrt data to upload.xlsx'
AMBER_FORCE_FIELD_PATH = '/Users/magdalena/opt/anaconda3/envs/py3/dat/leap'
ICM_PATH = '/lustre/tetyda/home/magdalu'
MOUNT_ICM_PATH = '/Users/magdalena/mount_point/to_mac'

EXTRACT_FRAMES_PDB_TCL = '/Users/magdalena/PycharmProjects/residence-time-prediction/src/feature_generation/' \
                         'step_1_extract_xyz_data/vmd_extract_frames_into_different_pdb.tcl'

EXTRACT_LIGAND_COM_TCL = '/Users/magdalena/PycharmProjects/residence-time-prediction/src/feature_generation/step_1_extract_xyz_data/vmd_com.tcl '

# VARS
PDB_TO_DO = {
    # '6EYA': 'C4K', #A/B
    # '3BJM': 'BJM',
    # '4DAJ': '0HK',
    # '4DQB': '017',
    # '4OHU': '2TK',
    # '4OYR': '1US',
    # '5COQ': 'TCU',
    # '5J20': '6FJ',
    # '5J27': '6FF',
    # '5J2X': '6DL',  # A/B
    # '5J64': '6G7',
    # '5J86': '6GW',
    # '5J9X': '6GC',
    # '5LNZ': '70Z',  # A/B
    # '5MTR': 'XT0',
    # '5NYH': '9EK',
    # '5OCI': '9R8',
    # '5OD7': 'H0T',
    # '5ODX': '9RZ',
    # '5UGS': 'XT5',  # A/B
    # '5UGT': 'XTW',
    # '5UGU': 'XTV',
    # '6B1E': 'LF7',
    # '6DJ1': 'AB1'  # A/B
}

ab = ['6EYA', '5J2X', '5LNZ', '5UGS', '6DJ1', '2YKJ']

VMD_PDB = {
    '1QSG': 'TCL',
    '1XKK': 'FMM',
    '1YET': 'GDM',
    '2BSM': 'BSM',
    '2UWD': '2GG',
    '2VCI': '2GJ',
    '2VCJ': '2EQ',
    '2X22': 'TCU',
    # '2X23': 'TCU',
    '2YKI': 'YKI',
    # '2YKJ': 'YKJ',  # A/B
    '3EKX': '1UN',
    '4OIM': 'JUS',
    # '4OXY': '1TN',
    # '5LNY': '70K',
    '5LO5': '70M',
    '5LO6': '70O',
    '5LQ9': '72K',
    '5LR1': '72Y',
    '5LR7': '73J',
    '5LRZ': '73Y', # ares
    '5LS1': '73Z',
    # '5MTP': '53K',
    # '5MTQ': 'XT3',
    '5NYI': '2EQ', # ares
    '5T21': '74E', # ares
    '6EI5': 'B5Q',
    # '6EL5': 'PU1',
    # '6ELN': 'P4A',
    # '6ELO': 'BAW',
    # '6ELP': 'BA8',
    # '6EY8': 'C4T',
    # '6EY9': 'C4N',
    # '6EYB': 'C3Z',
    # '6F1N': 'C8W',
}

PDB_KOKH = [
    '2BSM', '2UWD', '2VCI', '2YKI', '2YKJ', '5LO5', '5LO6', '5LQ9',
    '5LR1', '5LR7', '5LRZ', '5LS1', '5NYI', '5T21', '6EI5', '6EL5',
    '6ELN', '6ELO', '6ELP', '6EY8', '6EY9', '6F1N'
]

PDB_ONLY_KOKH = {
    '2BSM': 'BSM',
    '2UWD': '2GG',
    '2VCI': '2GJ',
    '2YKI': 'YKI',
    '5LO5': '70M',
    '5LO6': '70O',
    '5LQ9': '72K',
    '5LR1': '72Y',
    '5LR7': '73J',
    '5LRZ': '73Y',  # ares
    '5LS1': '73Z',
    '5NYI': '2EQ', # ares
    '5T21': '74E', # ares
    '6EI5': 'B5Q', # ares
}

PDB_NOT_KOKH = {
    '1QSG': 'TCL',
    '1XKK': 'FMM',
    '1YET': 'GDM',
    '2VCJ': '2EQ',
    '2X22': 'TCU',
    '3EKX': '1UN',
    '4OIM': 'JUS',
}
