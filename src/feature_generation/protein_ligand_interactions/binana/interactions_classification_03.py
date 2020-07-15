import os
from typing import List

import pandas as pd

from src.utils.externals import OUTPUT_PATH, BINANA_INTERACTIONS_PATH


def get_pdb_ids(files_path: str):
    pdb_ids = []
    for root, dirs, filenames in os.walk(files_path):
        for name in dirs:
            pdb_ids.append(name)
    return pdb_ids


def get_output_file_by_pdb_id(pdb_id: str, output_path: str):
    return os.path.join(output_path, pdb_id, 'log.txt')


def classify(binana_file, idx):
    for _ in range(idx):
        next_line = next(binana_file).strip()
        if 'Raw data' in next_line:
            next_after_raw = next(binana_file).strip()
            if len(next_after_raw.strip()) == 0:
                return 0
            return 1


def check_if_interaction_exist(binana_file, interaction_type):
    if interaction_type == 'HB':
        for line in binana_file:
            if 'Hydrogen bonds:' in line:
                return classify(binana_file, 7)
    if interaction_type == 'APO':
        for line in binana_file:
            if 'Hydrophobic contacts (C-C):' in line:
                return classify(binana_file, 8)
    if interaction_type == 'ARO':
        for line in binana_file:
            if 'pi-pi stacking interactions:' in line:
                class_pi_pi = classify(binana_file, 6)
                if class_pi_pi == 1:
                    return class_pi_pi
            if 'T-stacking (face-to-edge) interactions:' in line:
                class_t = classify(binana_file, 7)
                if class_t == 1:
                    return class_t
    if interaction_type == 'IO':
        for line in binana_file:
            if 'Salt Bridges:' in line:
                class_salt = classify(binana_file, 3)
                if class_salt == 1:
                    return 1
            if 'Cation-pi interactions:' in line:
                class_cation_pi = classify(binana_file, 7)
                if class_cation_pi == 1:
                    return class_cation_pi


def create_interactions_dict(pdb_id: str, log_file: str):
    interaction_types = ['HB', 'APO', 'ARO', 'IO']
    interactions_dict = {
        'PDB ID': pdb_id
    }
    with open(log_file, 'r') as binana_file:
        for interaction_type in interaction_types:
            class_ = check_if_interaction_exist(binana_file, interaction_type)
            interactions_dict[interaction_type] = class_
    return interactions_dict


def create_list_of_dicts():
    interactions = []
    pdb_ids = get_pdb_ids(OUTPUT_PATH)
    for pdb_id in pdb_ids:
        log_file = get_output_file_by_pdb_id(pdb_id, OUTPUT_PATH)
        interactions_for_single_complex = create_interactions_dict(pdb_id, log_file)
        interactions.append(interactions_for_single_complex)
    return interactions


def create_csv(data: List):
    df = pd.DataFrame(data, dtype='int64')
    df.fillna(value=0, inplace=True)
    df.APO = df.APO.astype('int64')
    df.ARO = df.ARO.astype('int64')
    df.IO = df.IO.astype('int64')
    df.to_csv(os.path.join(BINANA_INTERACTIONS_PATH, 'interactions.csv'))


if __name__ == '__main__':
    interactions = create_list_of_dicts()
    create_csv(interactions)
