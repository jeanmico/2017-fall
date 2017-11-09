# generate regular expressions for searching the files

import os
# from subprocess import call

fname = "gc_tiny.tsv"
path = os.path.join(os.path.sep, 'Users', 'student', 'pollard', 
	'shattuck0', 'snayfach', 'collaborations', 'gut_mags', 'bin_qc')

pos_fname = "set_positive.csv"
neg_fname = "set_negative.csv"

pos = []
neg = []
with open(os.path.join(path, pos_fname)) as posfile:
	# read in the positive sample and bin ids
	for line in posfile.readlines()[1:]:
		temp = line.strip().split(',')
		regstr = temp[0] + "[[:blank:]]" + temp[1]  # TODO: fix the . in the regex pattern
		pos.append(regstr)
		# #grepstr = 'grep --color=never ' + regstr + ' ' + os.path.join(path, fname) + ' >> out.txt'
		# grepstr = ['grep', '--color=never', 'regstr', os.path.join(path, fname), '>>',  'out.txt']
		# call(grepstr, shell=True)

with open(os.path.join(path, "pos_pattern.txt"), "w+") as output:
	for item in pos:
		output.write("%s\n" % item)

# RUN THE FOLLOWING COMMAND:
# $grep --color=never -f pos_pattern.txt tetra_med.tsv >> output.txt
