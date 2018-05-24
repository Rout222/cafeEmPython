#limpar workspace
rm(list=ls())
library("RSNNS")
library(SDMTools)
#limpar tela
cat('\014')
if(length(dev.list()) != 0){
  dev.off()  
}
library(mlbench)
data(Sonar)
str(Sonar[, 1:10])
library(caret)
set.seed(998)
inTraining <- createDataPartition(Sonar$Class, p = .75, list = FALSE)
training <- Sonar[ inTraining,]
testing  <- Sonar[-inTraining,]

fitControl <- trainControl(## 10-fold CV
  method = "repeatedcv",
  number = 10,
  ## repeated ten times
  repeats = 10)
gbmFit1 <- train(Class ~ ., data = training, 
                 method = "mlp", 
                 trControl = fitControl,
                 ## This last option is actually one
                 ## for gbm() that passes through
                 verbose = FALSE)
confusionMatrix(data = predict(gbmFit1, testing), reference = testing$Class, mode = "prec_recall")