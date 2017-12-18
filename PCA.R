setwd("/Users/student/pollard/shattuck0/snayfach/collaborations/gut_mags/bin_qc")

#df = read.table("dataframe_contam.txt", sep='\t', header=TRUE)
df = read.table("simulation_complete.tsv", sep='\t', header=TRUE)
dim(df)
head(df, 10)

fraction_ones = table(df$label)[2]/table(df$label)[1] #pos labels/neg labels


# add columns of difference from mean
# df$tetra_diff = df$contig_tetra - df$mean_tetra
# df$gc_diff = df$contig_gc - df$mean_gc
# df$length_diff = df$contig_length - df$mean_length
# df$depth_diff = df$contig_depth - df$mean_depth

#set/modify labels
# the dataset was built with labels (1 for negative and 0 for positive)
# we can alter the labels here to test different relationships
#df$label = ifelse(df$contamination>90, 1, 0)

set.seed(100)#to be able to replicate random sampling later
set.seed(101)
df_subset = df[sample(nrow(df), 400000), ]

trainRows<-runif(nrow(df_subset))>0.25 #randomly put aside 25% of the data


train<-df_subset[trainRows,]
fraction_ones_train = table(train$label)[2]/table(train$label)[1]

test<-df_subset[!trainRows,]



#df[sample(nrow(df), 3), ]
#df_train = df_subset[, c("z_tetra", "z_gc", "z_cds", "z_depth", "label")][sample(nrow(df_subset), 10000), ]
df_train = train[, c("z_tetra", "z_gc", "z_cds",  "label")]

df.pca = prcomp(df_train[, 1:4], center=TRUE, scale. = TRUE)
df_test = df_subset[!df_train, ]
print(df.pca)

plot(df.pca, type="l")

summary(df.pca)
library(ggfortify)

jpeg('rplot.jpg')
autoplot(prcomp(df_train, data = df_train, colour="label"))
dev.off()

###LOGISTIC REGRESSION###
#mylogit = glm(label ~ z_tetra + z_gc + z_length + z_depth, data=train, family = "binomial")
features = c('z_tetra', 'z_gc', 'z_cds', 'z_depth')
mylogit = glm(label ~ z_tetra + z_cds + z_depth, data=train, family = "binomial")
mylogit = glm(label ~ z_tetra + z_cds + z_depth, data=train, family = "binomial")
mylogit = glm(label ~ z_tetra + z_cds + z_depth, data=train, family = "binomial")
mylogit = glm(label ~ z_tetra + z_cds + z_depth, data=train, family = "binomial")
mylogit = glm(label ~ z_tetra + z_gc + z_length + z_depth, data=train, family = "binomial")

summary(mylogit)

anova(mylogit, test = "Chisq")
library(ggplot2)
library(pscl)
library(InformationValue)
pR2(mylogit)

predicted <- plogis(predict(mylogit, test)) 

misClassError(test$label, predicted, threshold = optCutOff)
plotROC(test$label, predicted)
Concordance(test$label, predicted)
sensitivity(test$label, predicted, threshold = optCutOff)
specificity(test$label, predicted, threshold = optCutOff)

confusionMatrix(test$label, predicted, threshold = optCutOff)

