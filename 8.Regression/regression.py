# coding=gbk
from numpy import*
import matplotlib.pyplot as plt
import random

#标准回归函数和数据导入函数
def loadDataSet(fileName):
	'''加载数据 '''
	
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
	'''标准回归函数--->计算最佳拟合直线 '''
	xMat=mat(xArr)
	yMat=mat(yArr).T
	xTx=xMat.T*xMat
	if linalg.det(xTx)==0.0:#行列式==0，则不存在逆矩阵
		print('This matrix is singular,cannot do inverse')
		return
	ws=xTx.I*(xMat.T*yMat)
	
	return ws
	
def standRegresPlot():
	
	#xArr是样本数据，yArr是目标值
	xArr,yArr=loadDataSet('ex0.txt')

	#变量ws存放的是回归系数
	ws=regression.standRegres(xArr,yArr)
	'''
	xMat=mat(xArr)
	#真实值
	yMat=mat(yArr)
	#预测值
	yHat=xMat*ws
	#预测值与真实值之间的相关性--->度量预测值和真实值之间的匹配程度
	#print(corrcoef(yHat.T,yMat))
	'''
	xMat=mat(xArr)
	yMat=mat(yArr)
	fig=plt.figure(1)
	ax=fig.add_subplot(111)
	#原始数据
	ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0].flatten().A[0] )

	xCopy=xMat.copy()
	#是x的大小有序
	xCopy.sort(0) #每一个列看成一个个体，对每一列的数据进行排序
	yHat=xCopy*ws  

	ax.plot(xCopy[:,1],yHat,c='red')
	plt.show()

	
	

''' 
给出x空间的任意一点，计算出对应的预测值yHat
'''
#局部加权线性回归函数
def lwlr(testPoint,xArr,yArr,k=1.0):
	
	xMat=mat(xArr)
	yMat=mat(yArr).T
	m=shape(xMat)[0]
	#创建对角矩阵，局部加权的权重矩阵
	weights=mat(eye((m)))
	for j in range(m):
		#计算每个样本点对应的权重值
		diffMat=testPoint-xMat[j,:]
		weights[j,j]=exp( (diffMat*diffMat.T)/(-2.0*k**2) )
		
	xTx=xMat.T*(weights*xMat)
	if linalg.det(xTx)==0.0:
		print("This matrix is singular,cannot do inverse")
		return
	#对回归系数ws的一个估计
	ws=xTx.I*(xMat.T*(weights*yMat))
	return testPoint*ws
	

def lwlrTest(testArr,xArr,yArr,k=1.0):
	'''测试局部加权线性回归函数 '''
	m=shape(testArr)[0]
	yHat=zeros(m)
	for i in range(m):
		yHat[i]=lwlr(testArr[i],xArr,yArr,k)
	return yHat
	
	
def lwlrPlot():
	'''plot 局部线性加权回归的结果'''
	xArr,yArr=loadDataSet('ex0.txt')	
	yHat=lwlrTest(xArr,xArr,yArr,0.01)

	xMat=mat(xArr)
	srtInd=xMat[:,1].argsort(0)	#argsort()返回排序对象的下标
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
	
	
#将回归用于真实数据：用于预测鲍鱼的年龄
def rssError(yArr,yHatArr):
	'''用来分析误差大小 '''
	return ((yArr-yHatArr)**2).sum()
	

def predictAbaAge():
	
	abX,abY=loadDataSet('abalone.txt')
	yHat01=lwlrTest(abX[0:99],abX[0:99],abY[0:99],0.1)
	yHat1=lwlrTest(abX[0:99],abX[0:99],abY[0:99],1)
	yHat10=lwlrTest(abX[0:99],abX[0:99],abY[0:99],10)
	
	err01=rssError(abY[0:99],yHat01.T)
	err1=rssError(abY[0:99],yHat1.T)
	err10=rssError(abY[0:99],yHat10.T)
	
	print("训练误差：")
	print(err01)
	print(err1)
	print(err10)
	
	yHat01=lwlrTest(abX[100:199],abX[0:99],abY[0:99],0.1)
	yHat1=lwlrTest(abX[100:199],abX[0:99],abY[0:99],1)
	yHat10=lwlrTest(abX[100:199],abX[0:99],abY[0:99],10)
	
	err01=rssError(abY[100:199],yHat01.T)
	err1=rssError(abY[100:199],yHat1.T)
	err10=rssError(abY[100:199],yHat10.T)
	
	
	#测试误差
	print("测试误差")
	print(err01)
	print(err1)
	print(err10)
	
	
	
	
#岭回归
def ridgeRegres(xMat,yMat,lamda=0.2):
	'''用于计算回归系数、
	功能：实现给定lambda下的岭回归求解，如果没有指定lambda，则默认为0.2
	'''
	xTx=xMat.T*xMat
	denom=xTx+eye(shape(xMat)[1])*lamda
	if linalg.det(denom) == 0.0:
		print("This matrix is singular,cannot do inverse")
		return
	#如果矩阵非奇异时即det！=0,就计算回归系数并返回
	ws=denom.I*(xMat.T*yMat)
	return ws

	
def ridgeTest(xArr,yArr):
	'''用于在一组lamda上测试结果
		为了使用岭回归和缩减技术，首先需要对特征做标准化处理
	returns:
		wMat:得到30个不同的lamda所对应的回归系数
	'''
	xMat=mat(xArr)
	yMat=mat(yArr).T
	#中心化
	yMean=mean(yMat,0)#按列求均值
	yMat=yMat-yMean
	
	#所有特征都减去各自的均值并除以方差
	#所有特征标准化
	xMeans=mean(xMat,0)#按列求均值
	xVar=var(xMat,0) #按列求方差
	xMat=(xMat-xMeans)/xVar
	
	#测试了30个lamda
	numTestPts=30
	wMat=zeros( (numTestPts,shape(xMat)[1]) )
	for i in range(numTestPts):
		#lamda以指数级变化，这样可以看出lamda在取非常小的值和非常大的值时，分别对结果造成的影响
		ws=ridgeRegres(xMat,yMat,exp(i-10))
		wMat[i,:]=ws.T
	return wMat

def testRidgeAbaLone():
	'''在鲍鱼数据集上的运行结果 '''
	abX,abY=loadDataSet('abalone.txt')

	ridgeWeights=ridgeTest(abX,abY)
	print(shape(ridgeWeights)[1])
	
	fig=plt.figure(1)
	ax=fig.add_subplot(111)
	ax.plot(ridgeWeights)
	plt.show()
	
	
#前向逐步线性回归
def stageWise(xArr,yArr,eps=0.01,numIt=100):
	'''前向逐步线性回归
	parameters:
		xArr:样本数据
		yArr:目标值
		eps:表示每次迭代需要调整的步长
		numIt:表示迭代次数
	'''
	xMat=mat(xArr)
	yMat=mat(yArr).T
	#目标值中心化
	yMean=mean(yMat,0)
	yMat=yMat-yMean
	#特征数据标准化
	xMat=regularize(xMat)
	
	
	m,n=shape(xMat)
	returnMat=zeros((numIt,n))
	#初始化w
	#用来保存w的值
	ws=zeros( (n,1) )
	#为实现贪心算法建立ws的两份副本
	wsTest = ws.copy()
	wsMax=ws.copy()
	
	for i in range(numIt):
		print(ws.T)
		lowestError = inf#设置当前最小误差
		for j in range(n):#对于每个特征
			#每次改变一个特征
			for sign in [-1,1]:#增大或缩小
				#恢复到之前的数值，使得每个特征增加或减少一个步长
				wsTest=ws.copy()
				wsTest[j]+=eps*sign #改变w的一个系数得到一个新的w
				
				yTest=xMat*wsTest#在当前w下得到一个新的预测
				#预测值和真实值之间的误差
				rssE=rssError(yMat.A,yTest.A)
				if rssE<lowestError:
					lowestError = rssE
					wsMax=wsTest
					
		ws=wsMax.copy()
		returnMat[i,:]=ws.T
	return returnMat
					
			
def regularize(xMat):
	'''将特征数据标准化 '''
	xMean=mean(xMat,0)
	xVar=var(xMat,0)
	xMat=(xMat-xMean)/xVar
	return xMat
	
	
#下面使用交叉验证测试岭回归
def crossValidation(xArr,yArr,numVal=10):
	''' 使用交叉验证测试岭回归
	parameters:
		xArr:样本特征
		yArr:目标值
		numVar:交叉验证的次数
		
	
	'''
	m=len(yArr) #样本数
	indexList=range(m)
	errorMat=zeros((numVal,30))
	for i in range(numVal):#进行迭代的次数
		trainX=[]
		trainY=[]
		testX=[]
		testY=[]
		random.shuffle(indexList)#打乱一个列表
		for j in range(m):
			if j<m*0.9: #90%作为训练
				trainX.append(xArr[indexList[j]])
				trainY.append(yArr[indexList[j]])
			else:#10%作为测试
				testX.append(xArr[indexList[j]])
				testY.append(yArr[indexList[j]])
		#岭回归返回测试的30次的回归系数---》使用30个不同的lamda值创建了30组不同的回归系数
		wMat=ridgeTest(trainX,trainY)#岭回归
		for k in range(30):
			matTestX=mat(testX)
			'''此处的处理其实并不是很明白 '''
			matTrainX=mat(trainX)
			meanTrain=mean(matTrainX,0)
			varTrain=var(matTrainX,0)
			matTestX=(matTestX-meanTrain)/varTrain
			yEst=matTestX*mat(wMat[k,:]).T + mean(trainY)
			errorMat[i,k]=rssError(yEst.T.A,array(testY))
	#所有交叉验证完成之后	
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
