from typing import List

import numpy as np
import pandas as pd
from scipy.stats import norm

from utils import externals


def compute_tau(t):
    return (np.sort(t)[int(len(t) / 2.0 - 0.5)] + np.sort(t)[int(len(t) / 2)]) / 2.0


def bootstrapp(t, rounds=50000):
    alpha = 0.8
    sub_set = int(alpha * len(t))
    tau_bootstr = []
    for i in range(1, rounds):
        # generate a sub-set
        np.random.shuffle(t)
        t_b = t[:sub_set]
        # find residence time from a sub-stet
        t_b_sorted_50 = compute_tau(t_b)
        tau_bootstr.append(t_b_sorted_50)
    return tau_bootstr


def compute_times(pdb_list: List[str], df: pd.DataFrame) -> pd.DataFrame:
    for pdb_id in pdb_list:
        d_list = []
        times_set = {}

        for rep_num in range(1, 11):
            d_list.append(f'/Users/magdalena/PycharmProjects/residence-time-prediction/times/{pdb_id}/{pdb_id}_times_{rep_num}.dat')


        # for rep_num in range(1, 11):
        #     path, path_ab = get_path_to_ramd(pdb_id, rep_num)
        #     d_list.append(get_md_files(path, '.dat'))
        #
        #     if path_ab:
        #         d_list.append(get_md_files(path_ab, '.dat'))
        # import pdb; pdb.set_trace()
        times_path_list = d_list
        # times_path_list = [item for sublist in d_list for item in sublist]

        # convert frame number into time data , last position in array is median
        mu_set = []
        std_set = []
        for t, d in enumerate(times_path_list):
            with open(d) as f:
                read_data = f.readlines()
            times = []
            for r in read_data:
                times.append(int(r[r.find("EXIT:") + 6:r.find(">") - 2]))
            times = np.asarray(times) * 2 / 1000000.  # 1000

            # ==============   Bootstrapping and computation of tau for each replica==================

            bt2 = bootstrapp(times, rounds=50000)
            mu, std = norm.fit(bt2)

            mu_set.append(mu)
            std_set.append(std)

            times = np.append(times, [mu])

            times_set[d[-5]] = times

        df.loc[df['PDB ID'].str.upper() == pdb_id, 'Relative Residence Time [ns]'] = np.mean(mu_set)
        df.loc[df['PDB ID'].str.upper() == pdb_id, 'Relative Residence Time std'] = np.mean(std_set)
    return df
