# generate regular expressions for searching the files

import os

path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 
	'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc')

pos_fname = "set_positive.csv"
neg_fname = "set_negative.csv"

expressions = []
pos_list = []
pos_exact = []
with open(os.path.join(path, pos_fname)) as posfile:
	# read in the positive sample and bin ids
	for line in posfile.readlines()[1:]:
		temp = line.strip().split(',')
		bin_id = temp[1].split('.')
		regstr = temp[0] + "[[:blank:]]" + bin_id[0] + '\.' + bin_id[1] + "[[:blank:]]"
		expressions.append(regstr)
		pos_list.append(regstr)
		pos_exact.append("\t".join(str(x) for x in temp[0:2]))

neg_list = []
neg_exact = []
with open(os.path.join(path, neg_fname)) as negfile:
	# read in the positive sample and bin ids
	for line in negfile.readlines()[1:]:
		temp = line.strip().split(',')
		bin_id = temp[1].split('.')
		regstr = temp[0] + "[[:blank:]]" + bin_id[0] + '\.' + bin_id[1] + "[[:blank:]]"
		expressions.append(regstr)
		neg_list.append(regstr)
		neg_exact.append("\t".join(str(x) for x in temp[0:2]))

with open(os.path.join(path, "set_pattern.txt"), "w+") as output:
	for item in expressions:
		output.write("%s\n" % item)

with open(os.path.join(path, "set_pos.txt"), "w+") as output:
	for item in pos_list:
		output.write("%s\n" % item)

with open(os.path.join(path, "set_neg.txt"), "w+") as output:
	for item in neg_list:
		output.write("%s\n" % item)

with open(os.path.join(path, "exact_neg.txt"), "w+") as output:
	for item in neg_exact:
		output.write("%s\t\n" % item)

with open(os.path.join(path, "exact_pos.txt"), "w+") as output:
	for item in pos_exact:
		output.write("%s\t\n" % item)
# RUN THE FOLLOWING COMMAND:
# $grep --color=never -f pos_pattern.txt tetra_med.tsv >> output.txt
