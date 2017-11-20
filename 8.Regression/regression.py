# coding=gbk
from numpy import*
import matplotlib.pyplot as plt
import random

#��׼�ع麯�������ݵ��뺯��
def loadDataSet(fileName):
	'''�������� '''
	
	dataMat=[]
	labelMat=[]
	with open(fileName) as fr:
		for line in fr.readlines():
			lineArr=[]
			curLine=line.strip().split('\t')
			for i in range(len(curLine)-1):
				lineArr.append(float(curLine[i]))
			dataMat.append(lineArr)
			labelMat.append(float(curLine[-1]))
			
	return dataMat,labelMat


def standRegres(xArr,yArr):
	'''��׼�ع麯��--->����������ֱ�� '''
	xMat=mat(xArr)
	yMat=mat(yArr).T
	xTx=xMat.T*xMat
	if linalg.det(xTx)==0.0:#����ʽ==0���򲻴��������
		print('This matrix is singular,cannot do inverse')
		return
	ws=xTx.I*(xMat.T*yMat)
	
	return ws
	
def standRegresPlot():
	
	#xArr���������ݣ�yArr��Ŀ��ֵ
	xArr,yArr=loadDataSet('ex0.txt')

	#����ws��ŵ��ǻع�ϵ��
	ws=regression.standRegres(xArr,yArr)
	'''
	xMat=mat(xArr)
	#��ʵֵ
	yMat=mat(yArr)
	#Ԥ��ֵ
	yHat=xMat*ws
	#Ԥ��ֵ����ʵֵ֮��������--->����Ԥ��ֵ����ʵֵ֮���ƥ��̶�
	#print(corrcoef(yHat.T,yMat))
	'''
	xMat=mat(xArr)
	yMat=mat(yArr)
	fig=plt.figure(1)
	ax=fig.add_subplot(111)
	#ԭʼ����
	ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0].flatten().A[0] )

	xCopy=xMat.copy()
	#��x�Ĵ�С����
	xCopy.sort(0) #ÿһ���п���һ�����壬��ÿһ�е����ݽ�������
	yHat=xCopy*ws  

	ax.plot(xCopy[:,1],yHat,c='red')
	plt.show()

	
	

''' 
����x�ռ������һ�㣬�������Ӧ��Ԥ��ֵyHat
'''
#�ֲ���Ȩ���Իع麯��
def lwlr(testPoint,xArr,yArr,k=1.0):
	
	xMat=mat(xArr)
	yMat=mat(yArr).T
	m=shape(xMat)[0]
	#�����ԽǾ��󣬾ֲ���Ȩ��Ȩ�ؾ���
	weights=mat(eye((m)))
	for j in range(m):
		#����ÿ���������Ӧ��Ȩ��ֵ
		diffMat=testPoint-xMat[j,:]
		weights[j,j]=exp( (diffMat*diffMat.T)/(-2.0*k**2) )
		
	xTx=xMat.T*(weights*xMat)
	if linalg.det(xTx)==0.0:
		print("This matrix is singular,cannot do inverse")
		return
	#�Իع�ϵ��ws��һ������
	ws=xTx.I*(xMat.T*(weights*yMat))
	return testPoint*ws
	

def lwlrTest(testArr,xArr,yArr,k=1.0):
	'''���Ծֲ���Ȩ���Իع麯�� '''
	m=shape(testArr)[0]
	yHat=zeros(m)
	for i in range(m):
		yHat[i]=lwlr(testArr[i],xArr,yArr,k)
	return yHat
	
	
def lwlrPlot():
	'''plot �ֲ����Լ�Ȩ�ع�Ľ��'''
	xArr,yArr=loadDataSet('ex0.txt')	
	yHat=lwlrTest(xArr,xArr,yArr,0.01)

	xMat=mat(xArr)
	srtInd=xMat[:,1].argsort(0)	#argsort()�������������±�
	xSort=xMat[srtInd][:,0,:]
	
	fig=plt.figure(1)
	ax=fig.add_subplot(111)
	ax.plot(xSort[:,1],yHat[srtInd])
	ax.scatter(xMat[:,1].flatten().A[0],mat(yArr).T.flatten().A[0],\
				s=2,c='red')
	plt.show()
	
	
def plotWei():
	x=array([0.1*m for m in range(11)])
	
	k=0.5
	y=exp( (x-0.5)**2/(-2*k**2) )
	
	fig=plt.figure(1)
	ax=fig.add_subplot(111)
	ax.plot(x,y)
	plt.show()
	
	
#���ع�������ʵ���ݣ�����Ԥ�Ⱬ�������
def rssError(yArr,yHatArr):
	'''������������С '''
	return ((yArr-yHatArr)**2).sum()
	

def predictAbaAge():
	
	abX,abY=loadDataSet('abalone.txt')
	yHat01=lwlrTest(abX[0:99],abX[0:99],abY[0:99],0.1)
	yHat1=lwlrTest(abX[0:99],abX[0:99],abY[0:99],1)
	yHat10=lwlrTest(abX[0:99],abX[0:99],abY[0:99],10)
	
	err01=rssError(abY[0:99],yHat01.T)
	err1=rssError(abY[0:99],yHat1.T)
	err10=rssError(abY[0:99],yHat10.T)
	
	print("ѵ����")
	print(err01)
	print(err1)
	print(err10)
	
	yHat01=lwlrTest(abX[100:199],abX[0:99],abY[0:99],0.1)
	yHat1=lwlrTest(abX[100:199],abX[0:99],abY[0:99],1)
	yHat10=lwlrTest(abX[100:199],abX[0:99],abY[0:99],10)
	
	err01=rssError(abY[100:199],yHat01.T)
	err1=rssError(abY[100:199],yHat1.T)
	err10=rssError(abY[100:199],yHat10.T)
	
	
	#�������
	print("�������")
	print(err01)
	print(err1)
	print(err10)
	
	
	
	
#��ع�
def ridgeRegres(xMat,yMat,lamda=0.2):
	'''���ڼ���ع�ϵ����
	���ܣ�ʵ�ָ���lambda�µ���ع���⣬���û��ָ��lambda����Ĭ��Ϊ0.2
	'''
	xTx=xMat.T*xMat
	denom=xTx+eye(shape(xMat)[1])*lamda
	if linalg.det(denom) == 0.0:
		print("This matrix is singular,cannot do inverse")
		return
	#������������ʱ��det��=0,�ͼ���ع�ϵ��������
	ws=denom.I*(xMat.T*yMat)
	return ws

	
def ridgeTest(xArr,yArr):
	'''������һ��lamda�ϲ��Խ��
		Ϊ��ʹ����ع������������������Ҫ����������׼������
	returns:
		wMat:�õ�30����ͬ��lamda����Ӧ�Ļع�ϵ��
	'''
	xMat=mat(xArr)
	yMat=mat(yArr).T
	#���Ļ�
	yMean=mean(yMat,0)#�������ֵ
	yMat=yMat-yMean
	
	#������������ȥ���Եľ�ֵ�����Է���
	#����������׼��
	xMeans=mean(xMat,0)#�������ֵ
	xVar=var(xMat,0) #�����󷽲�
	xMat=(xMat-xMeans)/xVar
	
	#������30��lamda
	numTestPts=30
	wMat=zeros( (numTestPts,shape(xMat)[1]) )
	for i in range(numTestPts):
		#lamda��ָ�����仯���������Կ���lamda��ȡ�ǳ�С��ֵ�ͷǳ����ֵʱ���ֱ�Խ����ɵ�Ӱ��
		ws=ridgeRegres(xMat,yMat,exp(i-10))
		wMat[i,:]=ws.T
	return wMat

def testRidgeAbaLone():
	'''�ڱ������ݼ��ϵ����н�� '''
	abX,abY=loadDataSet('abalone.txt')

	ridgeWeights=ridgeTest(abX,abY)
	print(shape(ridgeWeights)[1])
	
	fig=plt.figure(1)
	ax=fig.add_subplot(111)
	ax.plot(ridgeWeights)
	plt.show()
	
	
#ǰ�������Իع�
def stageWise(xArr,yArr,eps=0.01,numIt=100):
	'''ǰ�������Իع�
	parameters:
		xArr:��������
		yArr:Ŀ��ֵ
		eps:��ʾÿ�ε�����Ҫ�����Ĳ���
		numIt:��ʾ��������
	'''
	xMat=mat(xArr)
	yMat=mat(yArr).T
	#Ŀ��ֵ���Ļ�
	yMean=mean(yMat,0)
	yMat=yMat-yMean
	#�������ݱ�׼��
	xMat=regularize(xMat)
	
	
	m,n=shape(xMat)
	returnMat=zeros((numIt,n))
	#��ʼ��w
	#��������w��ֵ
	ws=zeros( (n,1) )
	#Ϊʵ��̰���㷨����ws�����ݸ���
	wsTest = ws.copy()
	wsMax=ws.copy()
	
	for i in range(numIt):
		print(ws.T)
		lowestError = inf#���õ�ǰ��С���
		for j in range(n):#����ÿ������
			#ÿ�θı�һ������
			for sign in [-1,1]:#�������С
				#�ָ���֮ǰ����ֵ��ʹ��ÿ���������ӻ����һ������
				wsTest=ws.copy()
				wsTest[j]+=eps*sign #�ı�w��һ��ϵ���õ�һ���µ�w
				
				yTest=xMat*wsTest#�ڵ�ǰw�µõ�һ���µ�Ԥ��
				#Ԥ��ֵ����ʵֵ֮������
				rssE=rssError(yMat.A,yTest.A)
				if rssE<lowestError:
					lowestError = rssE
					wsMax=wsTest
					
		ws=wsMax.copy()
		returnMat[i,:]=ws.T
	return returnMat
					
			
def regularize(xMat):
	'''���������ݱ�׼�� '''
	xMean=mean(xMat,0)
	xVar=var(xMat,0)
	xMat=(xMat-xMean)/xVar
	return xMat
	
	
#����ʹ�ý�����֤������ع�
def crossValidation(xArr,yArr,numVal=10):
	''' ʹ�ý�����֤������ع�
	parameters:
		xArr:��������
		yArr:Ŀ��ֵ
		numVar:������֤�Ĵ���
		
	
	'''
	m=len(yArr) #������
	indexList=range(m)
	errorMat=zeros((numVal,30))
	for i in range(numVal):#���е����Ĵ���
		trainX=[]
		trainY=[]
		testX=[]
		testY=[]
		random.shuffle(indexList)#����һ���б�
		for j in range(m):
			if j<m*0.9: #90%��Ϊѵ��
				trainX.append(xArr[indexList[j]])
				trainY.append(yArr[indexList[j]])
			else:#10%��Ϊ����
				testX.append(xArr[indexList[j]])
				testY.append(yArr[indexList[j]])
		#��ع鷵�ز��Ե�30�εĻع�ϵ��---��ʹ��30����ͬ��lamdaֵ������30�鲻ͬ�Ļع�ϵ��
		wMat=ridgeTest(trainX,trainY)#��ع�
		for k in range(30):
			matTestX=mat(testX)
			'''�˴��Ĵ�����ʵ�����Ǻ����� '''
			matTrainX=mat(trainX)
			meanTrain=mean(matTrainX,0)
			varTrain=var(matTrainX,0)
			matTestX=(matTestX-meanTrain)/varTrain
			yEst=matTestX*mat(wMat[k,:]).T + mean(trainY)
			errorMat[i,k]=rssError(yEst.T.A,array(testY))
	#���н�����֤���֮��	
	meanErrors=mean(errorMat,0)
	minMean=float(min(meanErrors))
	bestWeights=wMat[nonzero(meanErrors==minMean)]
	
	xMat=mat(xArr)
	yMat=mat(yArr).T
	meanX=mean(xMat,0)
	varX=var(xMat,0)
	
	unReg=bestWeights/varX
	print('the best model from Ridge Regression is : %f\n', %unReg)
	print("with constant term:"+str(-1*sum(multiply(meanX,unReg))+mean(yMat) ))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
