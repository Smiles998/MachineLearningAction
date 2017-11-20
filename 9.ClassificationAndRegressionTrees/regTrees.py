#coding=gbk
from numpy import*

def loadDataSet(filename):
	'''加载数据
	parameters:
		filename:数据文件的名称
	returns:
		dataMat:得到的数据列表
	'''
	dataMat=[]
	with open(filename) as fr:
		for line in fr.readlines():
			curLine=line.strip().split('\t')
			fltLine=list(map(float,curLine))#将每行的内容保存成一组浮点数
			dataMat.append(fltLine)
			
	return dataMat


def binSplitDataSet(dataSet,feature,value):
	''' 根据feature的特征值value将数据集分成两个集合
	   在给定特征和特征值的情况下，该函数通过数据过滤的方式将上述数据集合切分得到两个自己并返回
	parameters:
		dataSet:数据集合
		feature:进行集合划分的特征（待切分的特征）
		value:feature的特征值
	returns:
		mat0: >value的所有数据
		mat1: <=value的所有数据
	'''
	mat0=dataSet[nonzero(dataSet[:,feature] > value)[0],:]
	mat1=dataSet[nonzero(dataSet[:,feature] <= value)[0],:]
	return mat0,mat1



def regLeaf(dataSet):
	''' 负责生成叶节点，当chooseBestSplit()函数确定不再对数据进行切分时，将调用该函数得到叶节点的模型
	在回归树中，该模型其实就是目标变量的均值
	parameters:
		dataSet:数据集
	returns:
		返回数据集最后一列的均值
	'''
	return mean(dataSet[:,-1])
	
def regErr(dataSet):
	'''误差估计函数：该函数在给定数据上计算目标变量的平方误差
	parameters:
		dataSet:数据集
	returns:
		返回数据集最后一列的总方差
	'''
	return var(dataSet[:,-1])*shape(dataSet)[0]
	
	
#给定某个误差计算方法，该函数会找到数据集最佳的二元切分方法
def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
	''' 该函数需要完成两件事：用最佳方式切分数据集和生成相应的叶节点
	   该函数的目标是找到数据集切分的最佳位置：它遍历所有的特征及其可能的取值来找到使误差最小化的切分阈值
	parameters:
		dataSet:数据集
		leafType:是对创建叶节点的函数的引用
		errType：是对总方差计算函数的应用
		opt:是一个用户定义的参数构成的元组，用以完成树的构建
	returns:
		bestIndex：切分特征
		bestValues：切分特征值
	'''		
	tolS=ops[0]#允许的误差下降值
	tolN=ops[1]#切分的最少样本数

	if len( set( dataSet[:,-1].T.tolist()[0] ) )==1:
		#如果所有目标值相等则退出，构建叶节点
	#	print("1.相等")
		return None,leafType(dataSet)
		
	m,n=shape(dataSet)
	#print("m,n: %d,%d" %(m,n))
	#求出当前数据集中目标值的总方差
	S=errType(dataSet)
	#print("S:"+str(S))
	bestS=inf
	bestIndex=0
	bestValue=0
	
	for featIndex in range(n-1):#对于每个特征
	#	print("featIndex:%d" %featIndex)
	#	print(set(   dataSet[:,featIndex].T.tolist()[0])   )
	#	print(set(   dataSet[:,featIndex].T.tolist()[0]) )
		for splitVal in set(dataSet[:,featIndex].T.tolist()[0]):#对于特征的每个取值
			mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
			#tolN切分的最少样本数
			if(shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN):
				continue
			#切分之后的两个数据集的总方差
			newS=errType(mat0)+errType(mat1)
		#	print("newS:"+str(newS))
			if (newS < bestS):
			#	print("newS<bestS")
				bestIndex=featIndex
				bestValue=splitVal
				bestS=newS
		#		print("bestS:" +str(bestS))
		#		print("bestValues:"+str(bestValue)+"\n\n")
				
	#总方差和 组间总方差，tolS为允许的误差下降值
	if (S-bestS)<tolS: #如果误差不大则退出
	#	print("bestS: "+str(bestS))
	#	print("2.误差不大")
	#	print(S-bestS)
		return None,leafType(dataSet)
		
	#print("bestValue:"+str(bestValue))	
	mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)

	#print(shape(mat0)[0])
	#print(shape(mat1)[0])
	if(shape(mat0)[0] < tolN) or (shape(mat1)[0]<tolN):#如果切分的数据集很小则退出
	#	print("3.切分的数据集很小")
		return None,leafType(dataSet)
	#print("bestIndex:" +str(bestIndex))
	#print("bestValue:"+str(bestValue))
	return bestIndex, bestValue


#树构建函数
def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
	'''递归构建树的过程
	parameters:
		dataSet:数据集
		leafType:给出了建立叶节点的函数
		errType: 代表误差计算函数
		ops:是一个包含树构建所需其他参数的元组
	returns:
		retTree返回构建的树的根节点root
	'''
	#选择最为合适的切分特征和特征值
	#如果满足停止条件，该函数会返回None和某类模型的值
	#如果构建的是回归树，该模型是一个常数，如果是模型数，其模型是一个线性方程
	feat,val=chooseBestSplit(dataSet,leafType,errType,ops)
	if feat==None:return val #叶节点就只是一个值
	
	retTree={}
	retTree['spInd']=feat #划分特征
	retTree['spVal']=val  #特征值
	#根据划分特征和特征值将数据集划分为两个集合
	lSet,rSet=binSplitDataSet(dataSet,feat,val)
	#递归构建左子树和右子树的过程
	retTree['left']=createTree(lSet,leafType,errType,ops)
	retTree['right']=createTree(rSet,leafType,errType,ops)
	
	return retTree


#回归树剪枝函数
def isTree(obj):
	'''判断输入的节点是否为树节点或叶节点 ''' 
	return (type(obj).__name__=='dict')
	
	
def getMean(tree):
	'''返回该树左右子树中叶节点的值的均值 --->返回树平均值
	parameters:
		tree:树root节点
	returns：
		返回该树左右子树中叶节点的值的均值 	
	'''
	if isTree(tree['right']):#判断右子树是否为树
		tree['right']=getMean(tree['right'])
	if isTree(tree['left']):#判断左子树是否为树
		tree['left']=getMean(tree['left'])
	#返会左右子树叶节点的均值
	return (tree['left']+tree['right'])/2.0

#剪枝函数
def prune(tree,testData):
	'''树的剪枝函数
		使用后剪枝方法需要将数据集分成测试集合训练集，首先指定参数，使得构建出的树足够大，
	足够复杂，便于剪枝，接下来从上而下找到叶节点，用测试集来判断将这些叶节点合并是否能减低
	测试误差，如果是的话就合并
	--此种剪枝方法与《统计学习方法》中叙述的并不相同
	parameters:
		tree:待剪枝的树
		testData:剪枝所需的测试数据
	returns:
	
	'''
	#无测试样本则对数据进行塌陷处理
	if shape(testData)[0]==0:
		return getMean(tree)
	#因为树是由训练集生成的，所以测试集上会有一些样本与原数据集的取值范围不同
	if (isTree(tree['right'])) or isTree(tree['left']):
		#存在左右子树，则对测试数据集进行划分
		lSet,rSEt=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
	if isTree(tree['left']):
		#递归剪枝左子树
		tree['left']=prune(tree['left',lSet])
	if isTree(tree['right']):
		#递归剪枝右子树
		tree['right']=prun(tree['right'],rSet)
		
	#在对左右两个分支完成剪枝之后，还需要检查它们是否仍然是子树
	if not isTree(tree['left']) and not isTree(tree['right']):
		#不再是子树，则需要进行合并
		lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
		#未合并的误差
		errorNoMerge=sum(power(lSet[:,-1]-tree['left'],2))+\
						sum(power(rSet[:,-1]-tree['right'],2))
		treeMean=(tree['left']+tree['right'])/2.0
		#合并之后的误差
		errorMerge=sum(power(testData[:,-1]-treeMean,2))
		if errorMerge<errorNoMerge:
			#合并之后的误差小，则合并树
			print("merging")
			return treeMean  #成为叶节点
		else:
			#否则直接返回，不对其进行合并
			return tree
	else: 
		return tree   
		
#模型树的构建	
'''采用二元切分，构建模型树--->叶节点不再是简单的数值，取而代之的是一些线性模型 '''	
#模型树的叶节点生成函数--->生成的一个线性模型
def linearSolve(dataSet):
	'''将数据集格式化成目标变量和自变量，用于执行简单的线性回归
	parameters:
		dataSet:数据集
	returns:
		ws:回归系数
		X:自变量
		Y:目标变量
	'''
	m,n=shape(dataSet)
	X=mat(ones((m,n)))
	Y=mat(ones((m,1)))
	X[:,1:n]=dataSet[:,0:n-1]
	Y=dataSet[:,-1]
	xTx=X.T*X
	#矩阵的逆不存在也会造成程序异常
	if linalg.det(xTx)==0.0:
		raise NameError("This matrix is singular,cannot do inverse.\n\
						try increasing the second value of ops")
	ws=xTx.I*(X.T*Y)
	return ws,X,Y
	
def modelLeaf(dataSet):
	''' 求得数据的标准回归系数
	当数据不再需要切分的时候负责生成叶节点的模型
	parameters:
		dataSet:数据集
	returns:
		ws：标准回归系数
	'''
	ws,X,Y=linearSolve(dataSet)
	return ws
	
def modelErr(dataSet):
	''' 使用线性回归得出回归模型，并计算预测值与真实值之间的误差
	parameters:
		dataSet:数据集
	returns:
		回归模型的预测值和真实值之间的平方误差和
	
	'''
	ws,X,Y=linearSolve(dataSet)
	yHat=X*ws
	return sum(power(Y-yHat,2))


#用树回归进行预测的代码
def regTreeEval(model,inDat):
	'''回归树 --->在最后叶节点处为一个均值
	'''
	return float(model)

def modelTreeEval(model,inDat):
	'''模型树 
		在最后叶节点处是一个回归模型
	parameters:
		model:回归模型--->拟合的回归系数
		inDat:测试数据
	returns:
		返回回归模型预测的数据
	'''
	n=shape(inDat)[1] #特征数
	X=mat(ones((1,n+1)))
	X[:,1:n+1]=inDat
	return float(X*model)#返回预测的结果

#回归树和模型树的预测	
def treeForeCast(tree,inData,modelEval=regTreeEval):
	'''回归树和模型树的预测---->自顶向下遍历整棵树，直到命中叶节点为止
	parameters:
		tree:训练好的回归树或模型树
		inData:测试数据
		modelEval:树的类型-->进行预测的方式：指定树的类型，以便在叶节点上能够调用合适的模型
			：对叶节点数据进行预测的函数的引用
	returns:
		
	'''
	if not isTree(tree):
		#如果是叶节点，则直接进行预测
		return modelEval(tree,inData)
		
	#给定的数据的指定特征值>tree节点的特征阈值  
	#此时进入左子树
	if inData[tree['spInd']]>tree['spVal']:
		if isTree(tree['left']):
			return treeForeCast(tree['left'],inData,modelEval)
		else:
			return modelEval(tree['left'],inData)
	#给定的数据的指定特征值<=tree节点的特征阈值  
	#此时进入右子树
	else:
		if isTree(tree['right']):
			return treeForeCast(tree['right'],inData,modelEval)
		else:
			return modelEval(tree['right'],inData)


def createForeCast(tree,testData,modelEval=regTreeEval):
	'''多次调用treeForcast函数 
	parameters:
		tree:训练出来的树结构
		testData:测试数据
		modelEval:树类型
	returns:
		yHat:测试数据的预测结果
	'''
	m=len(testData)
	yHat=mat(zeros((m,1)))
	for i in range(m):
		yHat[i,0]=treeForeCast(tree,mat(testData[i]),modelEval)
	return yHat
			

 
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	












