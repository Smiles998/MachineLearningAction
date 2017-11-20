from numpy import *
import adaboost

dataMat,classLabels=adaboost.loadSimpData()

m=shape(dataMat)[0]
D=mat(ones((5,1))/m)
#adaboost.buildStump(dataMat,classLabels,D)
classifierArray=adaboost.adaBoostTrainDS(dataMat,classLabels,30)

#print(classifierArray)
#cf=adaboost.adaClassify([0,0],classifierArray )
#print(cf)

adaboost.TestHorseClic()
