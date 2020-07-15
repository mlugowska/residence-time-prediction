import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.externals import BINANA_INTERACTIONS_PATH

df = pd.read_csv(os.path.join(BINANA_INTERACTIONS_PATH, 'interactions.csv'), index_col=0)
df.set_index('PDB ID', inplace=True)
kendall = df.corr(method='kendall')
spearman = df.corr(method='spearman')
pearson = df.corr(method='pearson')

f, ax = plt.subplots(figsize=(18, 18))
sns.heatmap(pearson, annot=True, linewidths=.5, fmt='.1f', ax=ax)
plt.show()

df_t = df.transpose()
df_t.to_csv(os.path.join(BINANA_INTERACTIONS_PATH, 'interactions_transposed.csv'))