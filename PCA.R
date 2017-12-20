setwd("/Users/student/pollard/shattuck0/snayfach/collaborations/gut_mags/bin_qc/final")

#df = read.table("dataframe_contam.txt", sep='\t', header=TRUE)
df = read.table("simulation_sets.tsv", sep='\t', header=TRUE)
dim(df)
head(df, 10)

#add columns of difference from mean
df$tetra_diff = abs(df$tetra - df$mean_tetra)
df$gc_diff = abs(df$gc - df$mean_gc)
df$cds_diff = abs(df$cds - df$mean_cds)
df$depth_diff = abs(df$depth - df$mean_depth)

df$tetra_diff_mean = df$tetra_diff/df$mean_tetra
df$gc_diff_mean = df$gc_diff/df$mean_gc
df$cds_diff_mean = df$cds_diff/df$mean_cds
df$depth_diff_mean = df$depth_diff/df$mean_depth

df$log_gc = log2(df$gc/df$mean_gc)
df$log_tetra = log2(abs(df$tetra/df$mean_tetra))
df$log_cds = log2(df$cds/df$mean_cds)
df$log_depth = log2(df$depth/df$mean_depth)

set.seed(100)#to be able to replicate random sampling later

train = df[df$training == 1, ]
test<-df[df$training == 0, ]

# verify the split makes sense
print(dim(train)[1]/dim(df)[1]) # should be about .75
print(dim(unique(train[c("sample", "bin")]))) # should be 2994 bins

df_train = train[, c("z_tetra", "z_gc", "z_cds", "z_depth",  "label")]
df_test = train[, c("z_tetra", "z_gc", "z_cds", "z_depth",  "label")]

df.pca = prcomp(df_train[, 1:4], center=TRUE, scale. = TRUE)

print(df.pca)

plot(df.pca, type="l")

summary(df.pca)
library(ggfortify)

jpeg('rplot.jpg')
autoplot(prcomp(df_train, data = df_train, colour="label"))
dev.off()

###LOGISTIC REGRESSION###
#mylogit = glm(label ~ z_tetra + z_gc + z_length + z_depth, data=train, family = "binomial")


mylogit = glm(label ~ z_tetra + z_cds + z_depth, data=train, family = "binomial")
mylogit = glm(label ~ z_tetra + z_cds + z_depth, data=train, family = "binomial")
mylogit = glm(label ~ z_tetra + z_cds + z_depth, data=train, family = "binomial")
mylogit = glm(label ~ z_tetra + z_cds + z_depth, data=train, family = "binomial")
mylogit = glm(label ~ z_tetra + z_gc + z_cds + z_depth, data=train, family = "binomial")

features = c('log_gc', 'log_tetra', 'log_cds', 'log_depth')

modellist = lapply(features,
       function(x, d) glm(as.formula(paste("label ~ ", x, sep = " + ")), data = d), d = train)

summary(mylogit)

anova(mylogit, test = "Chisq")
library(ggplot2)
library(pscl)
library(InformationValue)
library(pROC)
pR2(mylogit)


for (x in 1:4){
  predicted = plogis(predict(modellist[[x]], test))
  plotROC(test$label, predicted, returnSensitivityMat = TRUE)
  roc_obj = roc(test$label, predicted)
  print(features[x])
  print(auc(roc_obj))
}


misClassError(test$label, predicted, threshold = optCutOff)
plotROC(test$label, predicted, returnSensitivityMat = TRUE)
Concordance(test$label, predicted)
sensitivity(test$label, predicted, threshold = optCutOff)
specificity(test$label, predicted, threshold = optCutOff)

confusionMatrix(test$label, predicted, threshold = optCutOff)

