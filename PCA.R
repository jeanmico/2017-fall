setwd("/Users/student/pollard/shattuck0/snayfach/collaborations/gut_mags/bin_qc")

df = read.table("dataframe_contam.txt", sep='\t', header=TRUE)
dim(df)
head(df, 10)

# add columns of difference from mean
df$tetra_diff = df$contig_tetra - df$mean_tetra
df$gc_diff = df$contig_gc - df$mean_gc
df$length_diff = df$contig_length - df$mean_length
df$depth_diff = df$contig_depth - df$mean_depth

#set/modify labels
# the dataset was built with labels (1 for negative and 0 for positive)
# we can alter the labels here to test different relationships
df$label = ifelse(df$contamination>90, 1, 0)

#df[sample(nrow(df), 3), ]
df_diff = df[, c("z_tetra", "z_gc", "z_length", "z_depth", "label")][sample(nrow(df), 10000), ]
#df_diff = df[, c("contig_tetra", "contig_gc", "contig_length", "contig_depth", "label")][sample(nrow(df), 10000), ]
#df_diff = df[, c("tetra_diff", "gc_diff", "length_diff", "depth_diff", "label")][sample(nrow(df), 10000), ]
df.pca = prcomp(df_diff[, 1:4], center=TRUE, scale. = TRUE)

print(df.pca)

plot(df.pca, type="l")

summary(df.pca)
library(ggfortify)

jpeg('rplot.jpg')
autoplot(prcomp(df_diff), data = df_diff, colour="label")
dev.off()

