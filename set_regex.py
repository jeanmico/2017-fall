# generate regular expressions for searching the files

import os
# from subprocess import call

fname = "gc_tiny.tsv"
path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 
	'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc')

pos_fname = "set_positive.csv"
neg_fname = "set_negative.csv"

expressions = []
with open(os.path.join(path, pos_fname)) as posfile:
	# read in the positive sample and bin ids
	for line in posfile.readlines()[1:]:
		temp = line.strip().split(',')
		bin_id = temp[1].split('.')
		regstr = temp[0] + "[[:blank:]]" + bin_id[0] + '\.' + bin_id[1]
		expressions.append(regstr)

with open(os.path.join(path, neg_fname)) as negfile:
	# read in the positive sample and bin ids
	for line in negfile.readlines()[1:]:
		temp = line.strip().split(',')
		bin_id = temp[1].split('.')
		regstr = temp[0] + "[[:blank:]]" + bin_id[0] + '\.' + bin_id[1]
		expressions.append(regstr)

with open(os.path.join(path, "set_pattern.txt"), "w+") as output:
	for item in expressions:
		output.write("%s\n" % item)

# RUN THE FOLLOWING COMMAND:
# $grep --color=never -f set_pattern.txt tetra_med.tsv >> output.txt
