# create two output files: set of positive MAGs and set of negative MAGs

import pandas as pd
import os

# filter parameters
pos_contam = 0
pos_complete = 90
neg_contam = 50
neg_complete = 90

fname = 'checkm.bin_qa.pre_qc.tsv'
path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc')
file_path = os.path.join(path, fname)
print(path)
df = pd.read_csv(file_path, sep='\t')

# output files: a list of positive MAGs and negative MAGs
pos_df = df[(df["completeness"] >= pos_complete) & (df["contamination"] == pos_contam)]
neg_df = df[(df["completeness"] > neg_complete) & (df["contamination"] > neg_contam)]

print(pos_df.count()) # why are my counts different from Stephen's?
print(neg_df.count())

# write pos and neg to output files
output = ["bin_id"]
pos_df.to_csv(os.path.join(path, "set_positive.csv"), columns=output)
neg_df.to_csv(os.path.join(path, "set_negative.csv"), columns=output)
