import trees

myDat,labels = trees.createDataSet()
print(myDat)

'''
myDat[0][-1] = 'maybe'
print(myDat)

shannonEnt = trees.calcShannonEnt(myDat)
print(shannonEnt)


splitSet = trees.splitDataSet(myDat,0,1)
print(splitSet)

bestFeature = trees.chooseBestFeatureToSplit(myDat)
print(bestFeature)

'''  

myTree = trees.createTree(myDat,labels)
print(myTree)
