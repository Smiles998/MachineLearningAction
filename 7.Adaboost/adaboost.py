# coding=gbk
from numpy import*


def loadSimpData():
	'''数据集 '''
	dataMat=matrix(
		[[1.,2.1],
		[2,1.1],
		[1.3,1.],
		[1.,1.],
		[2.,1.]])
	classLabels=[1.0,1.0,-1.0,-1.0,1.0]
	return dataMat,classLabels

#构建单层决策树--->弱分类器
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
	'''测试是否有某个值小于或者大于我们正在测试的阈值-----通过dimen指定样本数据中的某一个特征属性
	功能：通过阈值比较对数据进行分类
	parameters:
		dataMatrix:样本数据
		dimen:某一个特征的维度
		threshVal:特征阈值
		threshIneq:测试方式
	'''
	retArray=ones( (shape(dataMatrix)[0],1) )
	#将所有不满足不等式要求的元素设为-1
	if threshIneq=='lt':#lt---> '<'
		retArray[dataMatrix[:,dimen]<=threshVal] = -1.0#数组过滤
	else:#gt---> '>'
		retArray[dataMatrix[:,dimen]>threshVal] = -1.0
	return retArray
	
	
def buildStump(dataArr,classLabels,D):
	'''在一个加权数据集中循环，并找到具有最低错误率的单层决策树
	parameters:
		dataArr:训练样本
		classLabels:样本标签
		D:训练样本的权值
	returns:
		bestStump:最优单层决策树
		minError：最低错误率
		bestClasEst：在该决策树上的分类结果
	'''
	dataMatrix = mat(dataArr)
	labelMat = mat(classLabels).T
	m,n=shape(dataMatrix)
	
	numSteps=10.0     #用于在特征的所有可能值上进行遍历
	bestStump={}      #用于存储给定权重向量D时所得到的最佳单层决策树的相关信息
	bestClasEst=mat(zeros((m,1)))
	minError = inf    #开始初始化为正无穷大，之后用于寻找可能的最小错误率
	
	for i in range(n):#对于每一个特征
		rangeMin=dataMatrix[:,i].min()
		rangeMax=dataMatrix[:,i].max()
		stepSize=(rangeMax-rangeMin)/numSteps#求步长
		
		for j in range(-1,int(numSteps)+1): #将阈值设置为整个取值范围之外也是可以的
			for inequal in ['lt','gt']:#在大于和小于之间切换不等式
				#求得每个比值阶段的阈值
				threshVal=(rangeMin+float(j)*stepSize)
				
				predictedVals=stumpClassify(dataMatrix,i,threshVal,inequal)
				
				errArr=mat(ones( (m,1) ))
				errArr[predictedVals==labelMat]=0
				weightedError=D.T*errArr
				print('split:dim %d, thresh %.2f, thresh inequal:\
				%s, the weighted error is %.3f' %(i,threshVal,inequal,weightedError))
				
				if weightedError < minError:
					minError = weightedError
					bestClasEst=predictedVals.copy()
					bestStump['dim']=i
					bestStump['thresh']=threshVal
					bestStump['ineq']=inequal
	#print(bestStump)
	#print(minError)
	#print(bestClasEst)
	return bestStump,minError,bestClasEst
	
	
#基于单层决策树的AdaBoost训练过程
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
	'''AdaBoost的训练过程
	parameters:
		dataArr:训练样本
		classLabels:样本类别
		numIt:迭代次数
	 '''
	weakClassArr=[] #存放弱分类器
	m=shape(dataArr)[0] #样本数
	D=mat(ones((m,1))/m) #权重
	aggClassEst=mat(zeros((m,1)))#记录每个数据点的类别估计的累计值
	
	for i in range(numIt):
		#使用具有权值分布D的训练数据集学习，得到基本分类器
		bestStump,error,classEst=buildStump(dataArr,classLabels,D)
		print("D:")
		print(D.T)
		#计算基本分类器的系数
		alpha=float(0.5*log((1.0-error)/max(error,1e-16)))#防止出现分母为0的情况
		bestStump['alpha']=alpha
		weakClassArr.append(bestStump) #保存弱分类器
		
		print("classEst:")
		print(classEst.T)
		#更新权值
		expon=multiply(-1*alpha*mat(classLabels).T,classEst)
		D=multiply(D,exp(expon))
		D=D/D.sum()
		#构建基本分类器的线性组合
		aggClassEst+=alpha*classEst
		print("aggClassEst:")
		print(aggClassEst.T)
		
		aggErrors=multiply(sign(aggClassEst)!=mat(classLabels).T,ones((m,1)))
		errorRate=aggErrors.sum()/m
		print("total error:%.2f " %errorRate)
		if errorRate==0.0: break
		
	return weakClassArr
		
		
#AdaBoost分类函数
def adaClassify(dataToClass,classifierArr):
	''' AdaBoost分类函数
	parameters:
		dataToClass:待分类的数据
		clasifierArr:训练得出的弱分类器弱
	'''
	dataMatrix = mat(dataToClass)
	m=shape( dataMatrix )[0]
	aggClassEst = mat(zeros( (m,1) ))
	for i in range( len(classifierArr) ):
		classEst=stumpClassify(dataMatrix,classifierArr[i]['dim'],\
						classifierArr[i]['thresh'],classifierArr[i]['ineq'])
		aggClassEst += classifierArr[i]['alpha']*classEst
		print(aggClassEst)
	
	return sign(aggClassEst)
	 

#示例：在一个难数据集上应用AdaBoost
def loadDataSet(filename):
	''' 加载txt文本中的数据'''
	
	dataMat=[]
	labelMat=[]	
	with open(filename) as fr:
		for line in fr.readlines():
			lineArr=[]
			curLine=line.strip().split('\t')
			for i in range(len(curLine)-1):
				lineArr.append( float(curLine[i]) )
			dataMat.append(lineArr)
			labelMat.append(float(curLine[-1]))
	
	return dataMat,labelMat
			
def TestHorseClic():
	"""测试马疝病的死亡率 """
	dataArr,labelArr=loadDataSet('horseColicTraining2.txt')
	classifierArray=adaBoostTrainDS(dataArr,labelArr,100)
	
	testdataArr,testLabelArr=loadDataSet('horseColicTest2.txt')
	prediction=adaClassify(testdataArr,classifierArray)
	#得到测试样本数
	m=shape(testdataArr)[0]
	errorMat=ones((m,1))
	errorRatio = errorMat[prediction!=mat(testLabelArr).T].sum()/m
	print("测试错误率为：%.2f" %errorRatio)
	
	
	
	
	
	
	
	
		
