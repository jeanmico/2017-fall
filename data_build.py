import os
import pandas as pd


path = os.path.join(os.path.sep, "Users", "student", "pollard", "shattuck0", "snayfach", "collaborations", "gut_mags", "bin_qc")
bin_files = ["set_positive.csv", "set_negative.csv"]
files = ["tetra_sets.txt", "depth_sets.txt", "length_sets.txt"]

bin_pos = []
with open(os.path.join(path, bin_files[0])) as bins:
    for line in bins:
        bin_pos.append(line.strip().split(","))

bin_neg = []
with open(os.path.join(path, bin_files[1])) as bins:
    for line in bins:
        bin_neg.append(line.strip().split(","))


outname = "data_sets.txt"
headers = ["sample", "bin", "contig", "contig_length", "gc", "mean_gc", "std_gc", "z_gc", "tetra", "mean_tetra", "std_tetra", "z_tetra"]  # TODO insert LABEL column and other measures
with open(os.path.join(path, outname), "w+") as outfile:
    outfile.write(",".join(str(item) for item in headers))

contig_data = []
with open(os.path.join(path, "greptest.txt")) as gcfile:
    for line in gcfile:
        contig_data = []
        gc = line.strip().split()
        contig = gc[0:3]
        contig_data.append(gc)

        leave = False

        with open(os.path.join(path, "tetra_sets.txt")) as tetrafile:
            for line in tetrafile:
                tetra = line.strip().split()
                if tetra[0:3] == contig:
                    contig_data.append(tetra[4:])
                    leave = True
                if leave:
                    leave = False
                    break
        print(contig_data)
        with open(os.path.join(path, outname), "a") as output:
            output.write("\n")
            #output.write(",".join(str(item) for item in gc))
            #output.write(",")
            #output.write(",".join(str(item) for item in tetra[4:]))
            output.write(",".join(",".join(str(x) for x in measure) for measure in contig_data))

print(contig_data[0])
print(contig_data[1])
