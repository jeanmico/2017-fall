
# add contamination and completeness
awk '
BEGIN { FS=OFS="\t" }
{ k = $1 FS $2 }
NR==FNR { a[k]=$13 FS $14; next }
k in a { print $0, a[k] }
' checkm.bin_qa.pre_qc.tsv subset_neg.txt > subset_neg_contam.txt


# add contamination and completeness
awk '
BEGIN { FS=OFS="\t" }
{ k = $1 FS $2 }
NR==FNR { a[k]=$13 FS $14; next }
k in a { print $0, a[k] }
' checkm.bin_qa.pre_qc.tsv subset_pos.txt > subset_pos_contam.txt

#add numeric label column at the first position

awk 'BEGIN { FS=OFS="\t" } {print "1", $0}' subset_neg_contam.txt > subset_neg_contam_label.txt

awk 'BEGIN { FS=OFS="\t" } {print "0", $0}' subset_pos_contam.txt > subset_pos_contam_label.txt
