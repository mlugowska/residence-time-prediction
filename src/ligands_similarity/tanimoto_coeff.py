import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import rdFingerprintGenerator

from utils import externals
from utils.read_file import read_excel

df = read_excel(sheet_name='calculated')
PDBS = externals.PDB_NOT_KOKH  # PDB_ONLY_KOKH, PDB_NOT_KOKH, VMD_PDB

# Remove rows with structures not in use
# condition = ~df['PDB ID'].isin(PDBS.keys())
protein_name = 'InhA'
condition = df['Protein Name'] == protein_name
df.drop(df.loc[~condition].index, inplace=True)

# Creating molecules and storing in an array
molecules = []
for _, smiles in df[['Ligand SMILES']].itertuples():
    molecules.append((Chem.MolFromSmiles(smiles)))

# Creating fingerprints for all molecules
rdkit_gen = rdFingerprintGenerator.GetRDKitFPGenerator(maxPath=7)
fgrps = [rdkit_gen.GetFingerprint(mol) for mol in molecules]

# Calculating number of fingerprints
nfgrps = len(fgrps)
print("Number of fingerprints:", nfgrps)


# Defining a function to calculate similarities among the molecules
def pairwise_similarity(fingerprints_list, number_of_fingerprints):
    similarities = np.zeros((nfgrps, nfgrps))

    for i in range(1, number_of_fingerprints):
        similarity = DataStructs.BulkTanimotoSimilarity(fingerprints_list[i], fingerprints_list[:i])
        similarities[i, :i] = similarity
        similarities[:i, i] = similarity

    return similarities


# Calculating similarities of molecules
similarities = pairwise_similarity(fgrps, nfgrps)
tri_lower_diag = np.tril(similarities, k=0)

# Visulaizing the similarities

# definging labels to show on heatmap
# labels = PDBS.values()
labels = list(df['Ligand Code'])


def normal_heatmap(sim):
    # writing similalrities to a file
    f = open("similarities.txt", "w")
    print(similarities, file=f)

    sns.set(font_scale=0.8)

    # generating the plot
    plot = sns.heatmap(sim[:len(sim), :len(sim)], annot=True, annot_kws={"fontsize": 5}, center=0,
                       square=True, xticklabels=labels, yticklabels=labels, linewidths=.7, cbar_kws={"shrink": .5})

    plt.title('Heatmap of Tanimoto Similarities', fontsize=20)  # title with fontsize 20
    plt.show()

    # saving the plot
    fig = plot.get_figure()
    fig.savefig(f"tanimoto_heatmap_{protein_name}.png")


def lower_tri_heatmap(sim):
    f = open("similarities_lower_tri.txt", "w")

    print(tri_lower_diag, file=f)

    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    lower_tri_plot = sns.heatmap(tri_lower_diag[:len(sim), :len(sim)], annot=False, cmap=cmap, center=0,
                                 square=True, xticklabels=labels, yticklabels=labels, linewidths=.7,
                                 cbar_kws={"shrink": .5})

    plt.title('Heatmap of Tanimoto Similarities', fontsize=20)
    plt.show()

    fig = lower_tri_plot.get_figure()
    fig.savefig(f'tanimoto_heatmap_lw_tri_{protein_name}.png')


normal_heatmap(similarities)
lower_tri_heatmap(similarities)
