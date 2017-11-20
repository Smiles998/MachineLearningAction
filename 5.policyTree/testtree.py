import trees
import treePlotter

myDat,labels = trees.createDataSet()
print('labels:' +str(labels))

myTree = treePlotter.retrieveTree(0)
print('myTree: ' + str(myTree))
'''
classLabel = trees.classity(myTree,labels,[1,0])
print(classLabel)

classLabel1 = trees.classity(myTree,labels,[1,1])
print(classLabel1)
'''
trees.storeTree(myTree,'classifierStorage.txt')

tree1=trees.grabTree('classifierStorage.txt')
print(tree1)
