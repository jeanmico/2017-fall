import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

file_pre = 'gc_small'
fname = file_pre + '.tsv'
file_path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc', fname)

#gc_arr = np.genfromtxt(file_path, delimiter='\t', skip_header=1, dtype=['U15', 'U15', 'U15', 'i', 'f', 'f', 'f', 'f'], names=('id', 'bin_id', 'contig_id', 'length', 'contig_gc', 'mean_gc', 'std_gc', 'z_score'))
#print(gc_arr)
#print(gc_arr[3999, 0])
#print(gc_arr[3999, 1])
#print(gc_arr.shape())

gc = pd.read_csv(file_path, sep='\t')


# read in list of reference ids
ref_fname = "ref_genome_ids.txt"
ref_path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc', ref_fname)

ref_ids = {}
with open(ref_path) as ref_file:
    ref_ids = list(line.strip() for line in ref_file)


ref = gc[(gc["id"].isin(ref_ids))]
mag = gc[(~gc["id"].isin(ref_ids))]


# make a histogram of reference genome z-scores
plt.figure(0)
bins = np.linspace(0, 6, 100)
plt.hist(gc["z_score"], bins, label='mag', alpha = .5)
plt.hist(ref["z_score"], bins, label='ref', color='grey')
plt.title('z-score histogram - gc content')
plt.xlabel('z-score')
plt.legend(loc='upper right')
axes = plt.gca()
axes.set_yscale('log')
axes.set_xlim(left=0, right=6)
plt.savefig(file_pre + '_histogram.png', dpi=300)
