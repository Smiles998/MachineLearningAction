from math import log
import operator
import pickle


def createDataSet():
	''' 得到一个简单的数据集--->列表的列表'''
	dataSet = [ [1,1,'yes'],
				[1,1,'yes'],
				[1,0,'no'],
				[0,1,'no'],
				[0,1,'no'],	]	
	labels =['no surfacing','flippers']
	return dataSet,labels


#计算信息增益
#1.计算给定数据集的熵
def calcShannonEnt(dataSet):
	''' 计算给定数据集的熵 '''
	numEntries = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:  #统计各个类别的数目
		currentLabel = featVec[-1]#当前数据的类别
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
		
	shannonEnt = 0.0
	for key in labelCounts:   #???整个计算为什么不用矩阵运算，这样不是会更快一些么？
	#数据结构是字典
		prob = float(labelCounts[key])/numEntries
		shannonEnt -= prob*log(prob,2)  #以2为底求对数
	return shannonEnt    

#按照给定特征划分数据集--->不改变数据集dataSet
def splitDataSet(dataSet,feature,value):
	'''按照给定特征划分数据集 '''#调用：splitDataSet(myDat,0,1)
	'''
	parameters:
		dataSet:待划分的数据集
		axis:划分数据集的特征
		value:特征的取值	
	'''
	retDataSet = []
	for featVec in dataSet:
		if featVec[feature] == value: #去掉给定的特征
			reducedFeatVec = featVec[:feature]
			reducedFeatVec.extend(featVec[feature+1:])
			retDataSet.append(reducedFeatVec)
		
	return retDataSet#返回的数据集消耗了主特征（特征选择出来的划分特征）（进行了数据的复制）


#选择最好的数据集划分方式--->即选择最大信息增益的特征   （此处也不改变dataSet）
def chooseBestFeatureToSplit(dataSet):
	''' 选择最好的数据集划分方式'''
	numFeatures = len(dataSet[0])-1     #计算特征数
	baseEntropy = calcShannonEnt(dataSet)#计算数据集合dataSet的信息熵
	
	#存储最大信息增益 ，和获得最大信息增益的特征选择
	bestInfoGain = 0.0
	bestFeature = -1
	
	#对每个特征都计算信息增益
	for i in range(numFeatures):
		featList = [ example[i] for example in dataSet ]#每一个特征取值的列表
		uniqueVals = set(featList) #featList列表中的元素是unique的
		
		#计算特征中某个特征的条件熵--->第i个特征
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet,i,value) #从dataSet数据集中得到，某个特征=某个特征值的集合
			prob = len(subDataSet)/float(len(dataSet)) 
			newEntropy += prob*calcShannonEnt(subDataSet)
		#信息增益
		infoGain = baseEntropy - newEntropy
		if(infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
			
	return bestFeature


#在一群数据集中使用多数表决（vote）---->决定其分类
def majorityCnt(classList):
	'''投票表决-->多数决定其分类 '''
	'''
	parameters:
		classList:分类名称的列表
	'''
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted( classCount.items(),key=operator.itemgetter(1),reverse = True)
	return sortedClassCount[0][0] #返回其类别信息



#递归构建决策树---->ID3算法
'''
递归返回条件：
	1.每个分支下的所有实例都具有相同的分类，并将其作为分类标记
	2.程序遍历完所有划分数据集的属性，并将其实例数最大的类作为该类的分类标记
	3.最大信息增益<指定阈值（所有特征的信息增益都很小）	
'''
#实现过程中，逐步消耗特征，改变了labels，但是并没有改变dataSet数据集，而是每次划分都使用的副本
def createTree(dataSet,labels):
	'''ID3算法生成决策树 '''
	'''
	parameters:
		dataSet:数据集
		labels:标签列表包含了数据集中所有特征的标签--->也就是说（特征名称）'A','B','C',...
	'''
	classList = [ example[-1] for example in dataSet ]#得到所有数据实例的类别
	
	#条件1
	if classList.count(classList[0]) == len(classList):#所有实例是否属于同一个类别
		return classList[0] #返回其所属类别
	#条件2
	if len(dataSet[0]) ==1:
		return majorityCnt(classList)
		
	#找到最具有分类能力的特征	
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	
	#构建树结构---->字典数据结构
	myTree = { bestFeatLabel:{} }#构建特征根节点开始
	del(labels[bestFeat])#删除选中的标签---->消耗特征
	
	#选择出指定特征的所有取值，然后对数据集进行划分
	featValues = [ example[bestFeat] for example in dataSet ]
	uniqueVals = set(featValues)
	
	#对其每个子集调用递归
	for value in uniqueVals:
		subLabels = labels[:]#也使用的labels的副本
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)		
	return myTree
	

#使用决策树的分类函数---->使用决策树的分类器
def classity(inputTree,featLabels,testVec):
	'''使用决策树进行分类
	parameters:
		inputTree:决策树
		featLabels:
		testVec:测试样例	
	'''
	firstStr = list(inputTree.keys())[0]
	secondDict = inputTree[firstStr]
	#特征标签列表
	featIndex = featLabels.index(firstStr)
	
	for key in secondDict.keys():
		if testVec[featIndex] == key:#确定划分的数据集
			if type(secondDict[key]).__name__ == 'dict':
				classLabel = classity(secondDict[key],featLabels,testVec)
			else:
				classLabel = secondDict[key]
	return classLabel


def storeTree(inputTree,filename):
	"""将构造好的决策树存储到硬盘上
	parameters:
		inputTree:决策树
		filename: 存储文件名称
	"""
	with open(filename,'wb') as f:
		pickle.dump(inputTree,f);
		
def grabTree(filename):
	"""从硬盘上获取决策树模型 """
	with open(filename,'rb') as f:
		data = pickle.load(f)
	return data












