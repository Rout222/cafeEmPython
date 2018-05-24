#limpar workspace
rm(list=ls())
library("RSNNS")
library(SDMTools)
#limpar tela
cat('\014')
if(length(dev.list()) != 0){
  dev.off()  
}

dados <- read.table(
  "output.csv",
  header=T,
  sep=",",
  colClasses=c(rep("numeric",5), "numeric")
  )

padroniza <- function(s)
{
  retorno <- (as.double(s) - min(s))/(max(s) - min(s))
  
  return(retorno)
}

#funçoes basicas

x <- dados[,-length(dados)] # retira a classificação


y <- dados$Classe # classificaçao
#y <- factor(dados$Classe) # classificaçao


#gerar os gráficos
col <- c("DistanciaMaiorDefeito","AreaMinElipse","AreaMinRec","AreaMinCircle")

for (i in seq(1,length(x))) {
  df <- data.frame(x[i],y)
  colnames(df) <- c("x","y")  
}

indicesDeTreino = NULL
indicesDeTeste1 = NULL
indicesDeTeste2 = NULL

#separa os indices em 3 grupos, de 60%, 20%, 20%, por tipo
for (i in unique(y)) {
  indices = which(y==(i))
  indices = sample(indices)
  size    = length(indices)
  treino = 1:(floor(0.6*size))
  teste1 = (floor(0.6*size)+1):(floor(0.8*size))
  teste2 = (floor(0.8*size)+1):size
  indicesDeTreino = c(indicesDeTreino, indices[treino])
  indicesDeTeste1 = c(indicesDeTeste1, indices[teste1])
  indicesDeTeste2 = c(indicesDeTeste2, indices[teste2])
}

nNeuronios = 20
maxEpocas  = 30000

inputTeste =  data.frame( #input que eu usei em python
  x[,1],
  x[,2]/x[,5],
  x[,3]/x[,5],
  x[,4]/x[,5],
  x[,2]/x[,4],
  x[,2]/x[,3],
  x[,4]/x[,3]
)

for (i in seq(1,length(x))) {
  x[,i] = padroniza(x[,i])
}

for (i in seq(1,length(inputTeste))) {
  inputTeste[,i] = padroniza(inputTeste[,i])
}

RedeCa <- NULL
RedeCA<-mlp(x[indicesDeTreino,], y[indicesDeTreino], size=nNeuronios, maxit=maxEpocas, initFunc="Randomize_Weights",
            initFuncParams=c(-0.3, 0.3), learnFunc="Std_Backpropagation",
            learnFuncParams=c(0.051), updateFunc="Topological_Order",
            updateFuncParams=c(0), hiddenActFunc="Act_Logistic",
            shufflePatterns=F, linOut=TRUE)

plot(RedeCA$IterativeFitError,type="l",main="Erro da MLP CA")
print(paste( "Erro quadrado médio do treino modo 1, " ,mean(sqrt((y[indicesDeTreino]-predict(RedeCA, x[indicesDeTreino,]))^2))))

#testando rede com as entradas q eu tava testando no python
RedeCA2<- NULL
RedeCA2<-mlp(inputTeste[indicesDeTreino,], y[indicesDeTreino], size=nNeuronios, maxit=maxEpocas, initFunc="Randomize_Weights",
            initFuncParams=c(-0.3, 0.3), learnFunc="Std_Backpropagation",
            learnFuncParams=c(0.051), updateFunc="Topological_Order",
            updateFuncParams=c(0), hiddenActFunc="Act_Logistic",
            shufflePatterns=F, linOut=TRUE)

plot(RedeCA2$IterativeFitError,type="l",main="Erro da MLP CA")
print(paste( "Erro quadrado médio do treino, " ,mean(sqrt((y[indicesDeTreino]-predict(RedeCA2, inputTeste[indicesDeTreino,]))^2))))
