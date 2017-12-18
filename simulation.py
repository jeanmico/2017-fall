# script to build a simulation
# input: list of bins to use (these should be high-quality bins)
# process:
#  read in list of bins
#  group by the sample
#  for each sample
#   identify the contigs that can be added to the bins
#   for each bin in the sample:
#    select contigs and add them to the bin WITH LABELS
#    recalculate the feature stats
#    save output to file
# output: a tsv file containing the bins with contaminant contigs added
# this tsv file can then be used for a logistic regression model

import os
from collections import defaultdict
import subprocess
import json
import numpy as np

def generate_dicts(path, samples, contaminants):
    contigs_bad = defaultdict(list)
    contigs_good = defaultdict(list)
    i=0
    with open(os.path.join(path, "contig_lengths.tsv")) as lengths_file:
        for line in lengths_file:
            if i % 1000 == 0:
                print(i)
            i += 1
            values = line.strip().split()
            sample = values[0]
            bin_id = values[1]
            if sample in contaminants:
                if bin_id in contaminants[sample]:
                    contigs_bad[sample].append(bin_id + "\t" + str(values[2]) + "\t" + str(values[3]))
                else:
                    contigs_good[sample + "\t" + bin_id].append(str(values[2]) + "\t" + str(values[3]))
    with open(os.path.join(path, 'contigs_good.json'), 'w+') as good:
        json.dump(contigs_good, good)

    with open(os.path.join(path, 'contigs_bad.json'), 'w+') as bad:
        json.dump(contigs_bad, bad)

    print(len(contigs))

path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc')

# read in positive bins to be used
samples = defaultdict(list)
with open(os.path.join(path, "set_positive.tsv")) as sample_file:
        for line in sample_file.readlines()[1:]:
            sample = line.strip().split()[0]
            bin_id = line.strip().split()[1]
            samples[sample].append(bin_id)

# read in all bins from the positive samples
contaminants = defaultdict(list)
with open(os.path.join(path, "checkm.bin_qa.pre_qc.tsv")) as checkm_file:
    for line in checkm_file.readlines()[1:]:
        sample = line.strip().split()[0]
        bin_id = line.strip().split()[1]
        if sample in samples and  bin_id not in samples[sample]:
            contaminants[sample].append(bin_id)

if len(samples) != len(contaminants):
    # remove samples with only one bin; we cannot select contaminants for these
    sample_keys = set(samples.keys())
    contam_keys = set(contaminants.keys())
    diff = sample_keys.difference(contam_keys)
    for item in diff:
        samples.pop(item, None)
    #TODO write the #samples, #bins, and sample names to an output file

if len(samples) != len(contaminants):
    raise ValueError('sample dictionaries are of inequal length') #TODO: improve error message

new_dicts = False
if new_dicts:
    generate_dicts(path, samples, contaminants)

# otherwise, assume the contig length dictionaries have already been created
# read them
with open(os.path.join(path, 'contigs_bad.json')) as bad:
    contigs_bad = json.load(bad)
with open(os.path.join(path, 'contigs_good.json')) as good:
    contigs_good = json.load(good)

header = 'sample\torigin_bin\torigin_contig\tbin_id\tcontig\tlabel\tlength'
with open(os.path.join(path, 'simulation_contigs.tsv'), 'w+') as outfile:
    outfile.write(header + '\n')
for key, val in contigs_good.items():
    sample, bin_id = key.split('\t')
    bin_length = 0
    contig_list = []
    for item in val:
        contig, length = item.split("\t")
        bin_length += int(length)
        contig_list.append([sample, bin_id, contig, bin_id, contig, "0", length])
    target_min = .05
    target_max = .15
    contam_length = 0
    while contam_length/(contam_length + bin_length) < target_min:
        contig_select = contigs_bad[sample]
        i = np.random.randint(0, len(contig_select), 1)[0]
        new_bin, new_contig, new_length = contig_select[i].split('\t')
        contam_length += int(new_length)
        if contam_length/(contam_length + bin_length) > target_max:
            contam_length -= int(new_length)
        else:
            contig_list.append([sample, new_bin, new_contig, bin_id, "1" + new_contig, "1", new_length])
    with open(os.path.join(path, 'simulation_contigs.tsv'), "a") as outfile:
        outfile.write('\n'.join('\t'.join(str(x) for x in element) for element in contig_list))
        outfile.write('\n')


