import os
import numpy as np
from collections import defaultdict
import math

# reads in simulation_complete file
# adds column to indicate train or test
# assigns train/test values by bin
# outputs file to be used for logistic regression model creation

path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc')
filename = 'simulation_complete.tsv'

bin_dict = defaultdict(list)
with open(os.path.join(path, filename)) as infile:
    for line in infile:
        line_items = line.strip().split()
        if line_items[0] != 'sample':
            sample_bin = line_items[0] + '|' + line_items[3]
            bin_dict[sample_bin].append(line_items)

print(len(bin_dict))

simkey = str(np.random.randint(1000000, 1000000000000))

bin_count = len(bin_dict)
train_count = math.floor(bin_count * .75)
bin_list = list(bin_dict.keys())

train_bins = set(np.random.choice(bin_list, train_count, replace=False))

outname = "simulation_sets.tsv"
header = header = ['simulation', 'training', 'sample', 'origin_bin','origin_contig','bin', 'contig', 'label', 'length', 'gc', 'mean_gc', 'std_gc', 'z_gc', 'tetra', 'mean_tetra', 'std_tetra', 'z_tetra', 'depth', 'mean_depth', 'std_depth', 'z_depth', 'cds', 'mean_cds', 'std_cds', 'z_cds']
print(len(header))
with open(os.path.join(path, outname), 'w+') as outfile:
    outfile.write('\t'.join(x for x in header))
    outfile.write('\n')

for key, val in bin_dict.items():
    train = '0'
    if key in train_bins:
        train = '1'
    for item in val:
        with open(os.path.join(path, outname), 'a') as outfile:
            outfile.write(simkey + '\t' + train + '\t')
            outfile.write('\t'.join(str(x) for x in item))
            outfile.write('\n')
