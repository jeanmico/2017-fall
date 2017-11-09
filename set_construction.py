# reference files:
#  training set (set_positive.csv)
#  negative set (set_negative.csv)
# determine all contigs belonging to the training set
# determine all contigs belonging to the negative set
# build a matrix containing these contigs and their features
#  label (0 or 1, depending on the set)
#  contig length (distance from mean)
#  tetranucleotide frequency (distance from mean)
#  gc content (distance from mean)
#  read depth (distance from mean)
# where the mean refers to the mean of that bin
# 
# in R
#  generate logistic regression model
#  make PCA plot (colored by label of 0 or 1)

import os

fname = "tetra_tiny.tsv"
path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 
	'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc')

pos_fname = "set_positive.csv"
neg_fname = "set_negative.csv"

pos = []
neg = []
with open(os.path.join(path, pos_fname)) as posfile:
	# read in the positive sample and bin ids
	for line in posfile:
		pos.append(line.strip().split(','))
	#pos.append([i for i in line.strip().split() for line in posfile])

with open(os.path.join(path, neg_fname)) as negfile:
	# read in the negative sample and bin ids
	for line in negfile:
		neg.append(line.strip().split(','))


contigs = [["sample", "bin", "contig", "label", "tetra", "gc", "length", "depth"]]
# df = pd.DataFrame(columns=["sample_id", "bin_id", "label", "gc", "tetra", "length", "depth"])
# read in the tetranucleotide file
# DO NOT READ THE WHOLE FILE INTO MEMORY
# read one line, determine if it is a member of a set and process accordingly
with open(os.path.join(path, fname)) as file1:
	# make a list of the first two columns
	# determine if that list is a member of our set files and record or discard
	# correct last entry, distance from mean?
	for line in file1:
		temp = line.strip().split()
		if temp[0:2] in pos:
			contigs.append([temp[0], temp[1], temp[2], 1, float(temp[4]), float(temp[5])])
		if temp[0:2] in neg:
			contigs.append([temp[0], temp[1], temp[2], 0, float(temp[4]), float(temp[5])])

print(len(pos))
print(len(neg))
print(len(contigs))
# search other files for the list of lines we have made?
