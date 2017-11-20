import regTrees
from numpy import*

'''
testMat=mat(eye(4))
print(testMat)

mat0,mat1=regTrees.binSplitDataSet(testMat,1,0.5)
print("mat0:")
print(mat0)
print("mat1:")
print(mat1)

myDat=regTrees.loadDataSet('ex00.txt')
myMat=mat(myDat)
root=regTrees.createTree(myMat)
print(root)

myDat1=regTrees.loadDataSet('ex0.txt')
myMat1=mat(myDat1)
print(shape(myMat1))
root=regTrees.createTree(myMat1)
print(root)


#模型树的测试
myMat2=mat(regTrees.loadDataSet('exp2.txt'))
root=regTrees.createTree(myMat2,regTrees.modelLeaf,regTrees.modelErr,(1,10))
print(root)

'''

#比较树回归模型和普通的线性回归模型


trainMat=mat(regTrees.loadDataSet('bikeSpeedVsIq_train.txt'))
testMat=mat(regTrees.loadDataSet('bikeSpeedVsIq_test.txt'))

#创建一颗回归树
myTree=regTrees.createTree(trainMat,ops=(1,20))
yHat=regTrees.createForeCast(myTree,testMat[:,0])
r2=corrcoef(yHat,testMat[:,1],rowvar=0)[0,1]
print("-------------------")
print(r2)


#创建一颗模型树
myTree2=regTrees.createTree(trainMat,regTrees.modelLeaf,regTrees.modelErr,(1,20))
yHat=regTrees.createForeCast(myTree2,testMat[:,0],regTrees.modelTreeEval)
r22=corrcoef(yHat,testMat[:,1],rowvar=0)[0,1]
print("-------------------")
print(r22)


#使用标准线性回归模型
ws,X,Y=regTrees.linearSolve(trainMat)
m,n=shape(testMat)
yHat=zeros((m,1))
for i in range(m):
	yHat[i]=testMat[i,0]*ws[1,0]+ws[0,0]
	
r23=corrcoef(yHat,testMat[:,1],rowvar=0)[0,1]
print("-------------------")
print(r23)

















