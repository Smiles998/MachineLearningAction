# coding=gbk
from numpy import*


def loadSimpData():
	'''���ݼ� '''
	dataMat=matrix(
		[[1.,2.1],
		[2,1.1],
		[1.3,1.],
		[1.,1.],
		[2.,1.]])
	classLabels=[1.0,1.0,-1.0,-1.0,1.0]
	return dataMat,classLabels

#�������������--->��������
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
	'''�����Ƿ���ĳ��ֵС�ڻ��ߴ����������ڲ��Ե���ֵ-----ͨ��dimenָ�����������е�ĳһ����������
	���ܣ�ͨ����ֵ�Ƚ϶����ݽ��з���
	parameters:
		dataMatrix:��������
		dimen:ĳһ��������ά��
		threshVal:������ֵ
		threshIneq:���Է�ʽ
	'''
	retArray=ones( (shape(dataMatrix)[0],1) )
	#�����в����㲻��ʽҪ���Ԫ����Ϊ-1
	if threshIneq=='lt':#lt---> '<'
		retArray[dataMatrix[:,dimen]<=threshVal] = -1.0#�������
	else:#gt---> '>'
		retArray[dataMatrix[:,dimen]>threshVal] = -1.0
	return retArray
	
	
def buildStump(dataArr,classLabels,D):
	'''��һ����Ȩ���ݼ���ѭ�������ҵ�������ʹ����ʵĵ��������
	parameters:
		dataArr:ѵ������
		classLabels:������ǩ
		D:ѵ��������Ȩֵ
	returns:
		bestStump:���ŵ��������
		minError����ʹ�����
		bestClasEst���ڸþ������ϵķ�����
	'''
	dataMatrix = mat(dataArr)
	labelMat = mat(classLabels).T
	m,n=shape(dataMatrix)
	
	numSteps=10.0     #���������������п���ֵ�Ͻ��б���
	bestStump={}      #���ڴ洢����Ȩ������Dʱ���õ�����ѵ���������������Ϣ
	bestClasEst=mat(zeros((m,1)))
	minError = inf    #��ʼ��ʼ��Ϊ�������֮������Ѱ�ҿ��ܵ���С������
	
	for i in range(n):#����ÿһ������
		rangeMin=dataMatrix[:,i].min()
		rangeMax=dataMatrix[:,i].max()
		stepSize=(rangeMax-rangeMin)/numSteps#�󲽳�
		
		for j in range(-1,int(numSteps)+1): #����ֵ����Ϊ����ȡֵ��Χ֮��Ҳ�ǿ��Ե�
			for inequal in ['lt','gt']:#�ڴ��ں�С��֮���л�����ʽ
				#���ÿ����ֵ�׶ε���ֵ
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
	
	
#���ڵ����������AdaBoostѵ������
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
	'''AdaBoost��ѵ������
	parameters:
		dataArr:ѵ������
		classLabels:�������
		numIt:��������
	 '''
	weakClassArr=[] #�����������
	m=shape(dataArr)[0] #������
	D=mat(ones((m,1))/m) #Ȩ��
	aggClassEst=mat(zeros((m,1)))#��¼ÿ�����ݵ�������Ƶ��ۼ�ֵ
	
	for i in range(numIt):
		#ʹ�þ���Ȩֵ�ֲ�D��ѵ�����ݼ�ѧϰ���õ�����������
		bestStump,error,classEst=buildStump(dataArr,classLabels,D)
		print("D:")
		print(D.T)
		#���������������ϵ��
		alpha=float(0.5*log((1.0-error)/max(error,1e-16)))#��ֹ���ַ�ĸΪ0�����
		bestStump['alpha']=alpha
		weakClassArr.append(bestStump) #������������
		
		print("classEst:")
		print(classEst.T)
		#����Ȩֵ
		expon=multiply(-1*alpha*mat(classLabels).T,classEst)
		D=multiply(D,exp(expon))
		D=D/D.sum()
		#�����������������������
		aggClassEst+=alpha*classEst
		print("aggClassEst:")
		print(aggClassEst.T)
		
		aggErrors=multiply(sign(aggClassEst)!=mat(classLabels).T,ones((m,1)))
		errorRate=aggErrors.sum()/m
		print("total error:%.2f " %errorRate)
		if errorRate==0.0: break
		
	return weakClassArr
		
		
#AdaBoost���ຯ��
def adaClassify(dataToClass,classifierArr):
	''' AdaBoost���ຯ��
	parameters:
		dataToClass:�����������
		clasifierArr:ѵ���ó�������������
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
	 

#ʾ������һ�������ݼ���Ӧ��AdaBoost
def loadDataSet(filename):
	''' ����txt�ı��е�����'''
	
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
	"""�������޲��������� """
	dataArr,labelArr=loadDataSet('horseColicTraining2.txt')
	classifierArray=adaBoostTrainDS(dataArr,labelArr,100)
	
	testdataArr,testLabelArr=loadDataSet('horseColicTest2.txt')
	prediction=adaClassify(testdataArr,classifierArray)
	#�õ�����������
	m=shape(testdataArr)[0]
	errorMat=ones((m,1))
	errorRatio = errorMat[prediction!=mat(testLabelArr).T].sum()/m
	print("���Դ�����Ϊ��%.2f" %errorRatio)
	
	
	
	
	
	
	
	
		
