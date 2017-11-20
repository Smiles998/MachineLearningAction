from numpy import *
import matplotlib.pyplot as plt

#Logistic回归梯度上升优化算法
#目标函数形式为：z=w0x0+w1x1+w2x2+....+wnxn
def loadDataSet():
	'''从数据文件中得到数据集 --->列表形式'''
	dataMat=[]   #特征数据
	labelMat=[]  #标签
	with open('testSet.txt') as fr:
		for line in fr.readlines():		#readlines按行读取成为一个列表
			lineArr=line.strip().split()
			#此时增加了一个特征x0=1.0-->是为了统一目标函数的形式
			dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
			
			labelMat.append(int(lineArr[2]))
			
	return dataMat,labelMat
	
#sigmoid函数
def sigmoid(inX):
	return longfloat(1.0/(1+exp(-inX)))

#梯度上升算法
''' 此处必须将所有公式都进行推导，然后再进行详尽的理解，才能够读懂这些代码'''
def gradAscent(dataMtIn,classLabels):
	''' 梯度上升算法
	parameters:
		dataMtIn:2维的Numpy数组，每列分别代表每个不同的特征--->特征数组 （训练样本）
		classLabels:每个样本对应的类别标签
	returns:
		返回训练好的回归系数	
	'''
	#获得输入并将其转换为numpy矩阵
	dataMatrix=mat(dataMtIn)    #mat--->将输入解释为矩阵
	#transpose()在默认情况下是矩阵的转置
	labelMat=mat(classLabels).transpose()#默认行为为rows,cols相互颠倒
	#m为样本数，n为特征数
	m,n=shape(dataMatrix) #得到数据矩阵的rows, cols
	#步长
	alpha=0.001
	#迭代次数
	maxCycles=500
	weights=ones((n,1))  #初始化weights
	
	for k in range(maxCycles):#迭代直至收敛
		h=sigmoid(dataMatrix*weights)#此处的运算是矩阵运算-->h(x)
		error=(labelMat-h) 			 #误差
		weights=weights+alpha*dataMatrix.transpose()*error #根据梯度下降公式，这个地方是合理的
		
	return array(weights)#将矩阵转化为数组

#回执回归曲线
def plotBestFit(weights):
	#import matplotlib.pyplot as plt
#	weights = wei.getA()		#将一个矩阵返回成一个数组
	#加载数据和类别
	dataMat,labelMat = loadDataSet()
	dataArr = array(dataMat)
	#得到其样本个数
	m=shape(dataArr)[0]
	xcord1=[];ycord1=[]
	xcord0=[];ycord0=[]
	for i in range(m):
		if int(labelMat[i])==1:
			xcord1.append( dataArr[i,1] ) #？？？？此处的下标或许有问题
			ycord1.append( dataArr[i,2] )
		else:
			xcord0.append( dataArr[i,1] )
			ycord0.append( dataArr[i,2] )
	
	fig=plt.figure()
	ax=fig.add_subplot(111)
	#画散点图
	ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
	ax.scatter(xcord0,ycord0,s=30,c='green')
	x=arange(-3.0,3.0,0.1)
	y=( -weights[0]-weights[1]*x)/weights[2]
	ax.plot(x,y)
	plt.xlabel("X1")
	plt.ylabel("X2")
	plt.show()

#随机梯度算法--->相比于梯度算法具有一定的优势（记住：它们之间的差别）
def stocGradAscent0(dataMatrix,classLabels):
	''' 随机梯度算法'''
	#m样本个数,n特征数
	m,n=shape(dataMatrix)
	#步长
	alpha=0.01
	#所有回归系数初始化为1
	weights=ones(n)
	thrWei=weights #一个数组
	for j in range(200):
		for i in range(m):
			h=sigmoid(sum( dataMatrix[i]*weights ))  #数组乘法
			error=classLabels[i]-h
			weights = weights + alpha*error*dataMatrix[i] 
			thrWei=row_stack((thrWei,weights))#为数组增加一行

	return weights,thrWei
	
#改进之后的随机梯度算法
def stocGradAscent1(dataMatrix, classLabels, numIter=150):
	m,n=shape(dataMatrix)
	weights = ones(n)
	#求得迭代过程中所有的权重--》测试过程中使用
	#thrWei=weights #一个数组
	for j in range(numIter):
		dataIndex=list(range(m))
		for i in range(m):
			#步长的改变
			alpha = 4/(1.0+j+i)+0.01 
			#随机选取样本
			randIndex=int(random.uniform(0,len(dataIndex)) ) 
			h=sigmoid(sum(dataMatrix[randIndex]*weights))
			error=classLabels[randIndex]-h
			weights=weights+alpha*error*dataMatrix[randIndex]
			#thrWei=row_stack((thrWei,weights))#为数组增加一行
			del dataIndex[randIndex]
			
	return weights#,thrWei
	
	
	
#画出三个回归系数的变化情况
def drawWei(thrWei):
	fig1=plt.figure(2)
	ax1=plt.subplot(311)
	ax2=plt.subplot(312)
	ax3=plt.subplot(313)
	#m=shape(thrWei)[0]
	print(thrWei[:,0])
	ax1.plot(list(thrWei[:,0]))
	ax2.plot(list(thrWei[:,1]))
	ax3.plot(list(thrWei[:,2]))
	
	plt.show()

#示例：使用Logistic回归估计马疝病的死亡率

#Logistic回归分类函数
def classifyVecotr(inX, weights):
	prob=sigmoid(sum(inX*weights))
	if prob>0.5:
		return 1.0
	else:
		return 0.0

#测试算法	--->加载数据进行训练即可
def colicTest():
	''' 测试算法	--->加载数据进行训练即可'''
	trainingSet=[]
	trainingLabels=[]
	with open('horseColicTraining.txt') as frTrain,open('horseColicTest.txt') as frTest:
			for line in frTrain.readlines():
				currLine = line.strip().split('\t')
				lineArr=[]
				#将每个特征数据都转换为float，则不能对list整体float，则必须进行循环
				for i in range(21):
					lineArr.append(float(currLine[i]))
				trainingSet.append(lineArr)
				trainingLabels.append(float(currLine[21]))
			#训练模型，得到Logistics回归方程
			#每次训练的时候都是随机选取样本，因此每次的结果可能不太一样
			trainWeights= stocGradAscent1(array(trainingSet),trainingLabels,500)
			
			errorCount=0
			numTestVec=0.0
			for line in frTest.readlines():
				numTestVec +=1.0
				currLine=line.strip().split('\t')
				lineArr=[]
				for i in range(21):
					lineArr.append(float(currLine[i]))
				if int(classifyVecotr(array(lineArr),trainWeights)) !=int(currLine[21]):
					errorCount+=1
			errorRate=(float(errorCount)/numTestVec)
			print("the error rate of this test is : %f" %errorRate)
			return errorRate
			
		
def multiTest():
	numTests=10 #进行10次迭代与测试
	errorSum=0.0
	for k in range(numTests):
		errorSum+=colicTest()
	print("after %d iterations the average error rate is: %f" 
			%(numTests,errorSum/float(numTests)))#求得其平均错误率
				
			
				
	

