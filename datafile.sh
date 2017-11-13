awk '
BEGIN { FS=OFS="\t" }
{ k = $1 FS $2 FS $3 }
NR==FNR { a[k]=$5 FS $6 FS $7 FS $8; next }
k in a { print $0, a[k] }
' gc_sets.txt tetra_sets.txt > tetra_gc.txt


awk '
BEGIN { FS=OFS="\t" }
{ k = $1 FS $2 FS $3 }
NR==FNR { a[k]=$5 FS $6 FS $7 FS $8; next }
k in a { print $0, a[k] }
' length_sets.txt tetra_gc.txt > tetra_gc_length.txt

awk '
BEGIN { FS=OFS="\t" }
{ k = $1 FS $2 FS $3 }
NR==FNR { a[k]=$5 FS $6 FS $7 FS $8; next }
k in a { print $0, a[k] }
' depth_sets.txt tetra_gc_length.txt > tetra_gc_length_depth.txt

# output
# [tetra columns 1-8] [gc columns 5-8] [length columns 5-8] [depth columns 5-8]
