import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from MD_preparation.step_5_tau_analysis.check_corr_01 import add_labels, linear_regression_plus_correlation, create_xy
from utils import externals
from utils.calculate_residence_time import compute_times
from utils.read_file import read_excel

df = read_excel(sheet_name='calculated')
# df = df.dropna(subset=['Residence Time computed by Kokh [ns]'])
df = df.loc[:,
     ['PDB ID', 'Residence Time [s]', 'Residence Time Plus Minus [s]', 'Residence Time computed by Kokh [ns]']]
df.index = np.arange(1, len(df) + 1)

PDBS = externals.VMD_PDB
residence_times = compute_times(PDBS, df)
residence_times = residence_times.dropna(subset=["Relative Residence Time [ns]"])

# draw regplot()
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharey='row')
sns.regplot(data=residence_times, y='Residence Time computed by Kokh [ns]', x='Residence Time [s]', ax=ax1)
sns.regplot(data=residence_times.dropna(subset=["Residence Time computed by Kokh [ns]"]),
            y='Relative Residence Time [ns]', x='Residence Time [s]', ax=ax2)
sns.regplot(data=residence_times, y='Relative Residence Time [ns]', x='Residence Time [s]', ax=ax3, color="darkblue")

# Add PDB ID to plot's dots
add_labels(X=residence_times['Residence Time [s]'], y=residence_times['Residence Time computed by Kokh [ns]'], ax=ax1,
           pdb=PDBS)
data = residence_times.dropna(subset=["Residence Time computed by Kokh [ns]"])
add_labels(X=data['Residence Time [s]'], y=data['Relative Residence Time [ns]'], ax=ax2, pdb=externals.PDB_ONLY_KOKH)
add_labels(X=residence_times['Residence Time [s]'], y=residence_times['Relative Residence Time [ns]'], ax=ax3,
           pdb=externals.VMD_PDB)

# # Set label for x-axis
ax1.set_xlabel(' ', size=7)
ax2.set_xlabel(' ', size=7)
ax3.set_xlabel('τ exp [s]', size=10)

# # Set label for y-axis
ax2.set_ylabel('τ comp [ns]', size=10)
ax1.set_ylabel('', size=7)
ax3.set_ylabel('', size=7)

# # Set title for plot
ax1.set_title("Results from article", size=10)
ax2.set_title("Repeated on structures from article", size=10)
ax3.set_title("All structures", size=10)

ax1.set_ylim(0, 15)
ax2.set_ylim(0, 15)
ax3.set_ylim(0, 15)
plt.show()

# plt.savefig("check_only_kokh_2.png", dpi=300)
# plt.close(fig)
