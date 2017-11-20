from numpy import*

#SMO算法中的辅助函数
def loadDataSet(fileName):
	''' 加载数据
	parameters:
		fileName:数据文件名称
	returns:
		dataMat:data
		labelMat:class label
	'''
	dataMat=[]
	labelMat=[]
	with open(fileName) as fr:
		for line in fr.readlines():
			lineArr=line.strip().split('\t')
			dataMat.append( [float(lineArr[0]),float(lineArr[1])] )
			labelMat.append( float(lineArr[2]) )
		
	return array(dataMat),array(labelMat)
	

def selectJrand(i,m):
	''' 在[0,m)中随机进行选择，但选择的结果不能等于i
	parameters;
		i:是第一个alpha的下标
		m:是所有alpha的数目
	'''
	j=i
	while(j==i):
		j=int(random.uniform(0,m))
	return j
	
def clipAlpha(aj,H,L):
	'''用于调整大于H或小于L的alpha值,L<a<H,超过这个范围，则需要对其进行调整
	parameters:
		aj:经过裁剪之后的解
		H:解的最大值范围
		L：解的最小值范围
	'''
	if aj>H:
		aj=H
	if L>aj:
		aj=L
	return aj


def smoSimple(dataMatIn,classLabels,C,toler,maxIter):
	''' 一个简化版本的SMO算法
	parameters:
		dataMatIn:训练数据
		classLabels:训练样本的类别标签
		C:常数C
		toler:容错率
		maxIter:取消前最大的循环次数
	'''
	#将数组转化为矩阵，进行矩阵运算-->简化很多数学处理操作
	dataMatrix=mat(dataMatIn)
	labelMat=mat(classLabels).transpose()#此次进行了在转置-->列向量，对应于每个训练样本
	
	b=0
	#得到训练样本数（m）和特征数目（n）
	m,n=shape(dataMatrix)
	#构建一个alpha列矩阵，矩阵中的元素都初始化为0
	alphas=mat(zeros((m,1)))
	iterNum=0#该变量存储的是在没有任何alpha改变的情况下遍历数据集的次数
	while iterNum<maxIter:
		alphaPairsChanged=0#用于记录alpha是否已经进行了优化
		
		#该简化版本的SMO算法，选择两个优化变量时只是采用了一种最简单的方式--->按顺序选取
		for i in range(m):#遍历每个样本
			#预测类别-->对当前样本预测类别
			#.T表示转置  Multiply arguments element-wise.
			fXi=float( multiply(alphas,labelMat).T*\
					(dataMatrix*dataMatrix[i,:].T))+b
			#求得Ei		
			Ei=fXi-float(labelMat[i])#误差
			#如果误差很大，那么可以对该数据实例所对应的alpha值进行优化--->误差很大，则可对其进行优化
			if((labelMat[i]*Ei<-toler) and (alphas[i]<C) )or\
				( (labelMat[i]*Ei>toler) and (alphas[i]>0) ):
					j=selectJrand(i,m)   #任意选取一个其他的样本-->作为优化的第二个变量
					fXj=float( multiply(alphas,labelMat).T*\
						(dataMatrix*dataMatrix[j,:].T))+b
					Ej=fXj-float(labelMat[j])
					#得到需要优化的两个alpha
					alphaIold = alphas[i].copy() #python则会通过引用的方式传递所有列表，所以在需要旧值的时候，我们必须要对其进行保存，改变其的一个copy
					alphaJold = alphas[j].copy()
					#计算L和H
					if (labelMat[i]!=labelMat[j]):
						L=max(0,alphas[j]-alphas[i])
						H=min(C,C+alphas[j]-alphas[i])
					else:
						L=max(0,alphas[j]+alphas[i]-C)
						H=min(C,alphas[j]+alphas[i])
					if L==H:
						print('L==H')
						continue
					#Eta是alpha[j]的最优修改量 eta=K11+K22-2*K12
					eta=2.0*dataMatrix[i,:]*dataMatrix[j,:].T-\
						dataMatrix[i,:]*dataMatrix[i,:].T-\
						dataMatrix[j,:]*dataMatrix[j,:].T   
					#如果eta为0，则需要退出for循环的当前迭代过程
					if eta>=0:
						print("eta>=0")
						continue
					#未经裁剪过的alpha2
					alphas[j]-=labelMat[j]*(Ei-Ej)/eta
					#裁剪过的alpha2
					alphas[j]=clipAlpha(alphas[j],H,L)
					#如果alpha2的变化并不是很大，则重新进行选择
					if(abs(alphas[j]-alphaJold)<0.00001):
						print("j not moving enough")
						continue
					#计算alpha1
					alphas[i]+=labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
					#计算阈值b和差值Ei
					b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*\
						dataMatrix[i,:]*dataMatrix[i,:].T-\
						labelMat[j]*(alphas[j]-alphaJold)*\
						dataMatrix[i,:]*dataMatrix[j,:].T
					b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*\
						dataMatrix[i,:]*dataMatrix[j,:].T-\
						labelMat[j]*(alphas[j]-alphaJold)*\
						dataMatrix[j,:]*dataMatrix[j,:].T
					if (0<alphas[i]) and (C>alphas[i]):
						b=b1
					elif (0<alphas[j]) and (C>alphas[j]):
						b=b2
					else:
						b=(b1+b2)/2.0
					alphaPairsChanged+=1
					print("iterNum: %d i: %d,pairs changed %d" \
							%(iterNum,i,alphaPairsChanged))
							
							
		if(alphaPairsChanged==0):
			iterNum+=1
		else:
			iterNum=0 #只有在所有数据集上遍历maxIter次，且不再发生任何修改之后，程序才会停止并退出while循环
		print("iteration number: %d" %iterNum)
	return b,alphas
	

'''完整版Platt SMO的支持函数'''
'''不带核函数的optStruct
#建立一个数据结构来保存所有的重要值,这个过程可以通过一个对象来完成
#此处使用对象的目的并不是为了面向对象的编程，而只是作为一个数据结构来使用对象
class optStruct:
	def __init__(self,dataMatIn,classLabels,C,toler):
		self.X=dataMatIn			 		#训练样本
		self.labelMat = classLabels	 		#样本标签
		self.C=C					 		#常数C
		self.tol=toler				 		#容错度
		self.m=shape(dataMatIn)[0]   		#样本个数
		self.alphas=mat(zeros((self.m,1)))	#变量alphas
		self.b=0							#阈值b（截距b）
		self.eCache=mat(zeros((self.m,2)))  #eCache的第一列给出的是eCache是否有效的标志位，而第二列给出的是实际的E值
'''		

#核转换函数
def kernelTrans(X,A,kTup):
	m,n=shape(X)   
	K=mat(zeros( (m,1) ))
	if kTup[0]=='line':#线性核
		K=X*A.T
	elif kTup[0]=='rbf': #高斯径向基函数
		for j in range(m):
			deltaRow=X[j,:]-A
			K[j]=deltaRow*deltaRow.T
		K=exp(K/(-1*kTup[1]**2))
	else: raise NameError('Houston We Have a Problem--\
	That Kernel is not recognized')
	return K

class optStruct:
	def __init__(self,dataMatIn,classLabels,C,toler,kTup):
		''' kTup是一个包含核函数信息的元组'''
		self.X=dataMatIn					#训练样本
		self.labelMat=classLabels			#样本标签
		self.C=C							#常数C
		self.tol=toler						#容错度
		self.m = shape(dataMatIn)[0]		#样本个数
		self.alphas=mat(zeros((self.m,1)))	#变量alphas
		self.b=0							#阈值b（截距b）
		self.eCache = mat(zeros((self.m,2)))	#eCache的第一列给出的是eCache是否有效的标志位，而第二列给出的是实际的E值
		self.K=mat(zeros( (self.m,self.m) ))	#保存K(x,z)		
		for i in range(self.m):
			self.K[:,i]=kernelTrans(self.X,self.X[i,:],kTup)
	
	
'''		
#计算g(xk)	Ek=g(xk)-yi
def calcEk(oS,k):
	fxK=float(multiply(oS.alphas,oS.labelMat).T*\
			(oS.X*oS.X[k,:].T))+oS.b
	Ek=fxK-float(oS.labelMat[k]	)
	return Ek
'''
def calcEk(oS,k):
	fxk=float( multiply(oS.alphas,oS.labelMat).T*(oS.K[:,k])+oS.b)
	Ek=fxk-float(oS.labelMat[k])
	return Ek


#内循环的启发式方法	
def selectJ(i, oS, Ei):
	''' 内循环的启发式方法	-->选择第二个变量alpha值以保证在每次优化中采用最大步长
	
	parameters:
		i:第一个变量的下标 alphai
		oS:
		Ei: Ei=g(xi)-yi	
	returns:	
	'''
	maxk = -1  
	maxDeltaE = 0
	Ej = 0
	#将Ei在缓存中设置成为有效-->这里的有效意味着它已经计算好了
	oS.eCache[i] = [1,Ei] 
	#matrix.A-->Return self as an ndarray object
	#找出非零E值对应的alpha值
	validEcacheList = nonzero(oS.eCache[:,0].A)[0] #nonzero()函数的用法-->此处是为了求出非零元素的横坐标
	if len(validEcacheList)>1:
		for k in validEcacheList:
			if k==i: continue
			Ek = calcEk(oS,k)
			deltaE = abs(Ei-Ek)
			if deltaE>maxDeltaE:		 #选择具有最大步长的j
				maxk=k
				maxDeltaE=deltaE
				Ej=Ek
		return maxk,Ej
	else:
		j=selectJrand(i,oS.m)#如果是第一次循环的话，则随机选择一个alpha值
		Ej=calcEk(oS,j)	
	return j,Ej
	
	
	
def updateEk(oS,k):
	Ek=calcEk(oS,k)
	oS.eCache[k]=[1,Ek]

#完整Platt SMO算法中的优化例程
def innerL(i,oS):
	''' 用于寻找决策边界的优化例程
	parameters:
		i: 找到的第一个变量alphas[i]，相当于已经有了一个外层循环
		oS:重要数据的一个结构对象
	returns:
		1:表示有两个变量进行优化
		0：表示没有两个变量进行优化
	'''
	Ei=calcEk(oS,i) 
	#误差较大，则可以将其作为一个优化变量--->其实并没有看懂如何选择第一个优化变量
	if ((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i]*Ei > oS.tol) and (oS.alphas[i] > 0)): 	 
			
		j,Ej=selectJ(i,oS,Ei) #选择第二个优化变量
			
		alphaIold = oS.alphas[i].copy()
		alphaJold = oS.alphas[j].copy()
			
		if(oS.labelMat[i]!=oS.labelMat[j]):
			L=max( 0,oS.alphas[j]-oS.alphas[i] )
			H=min( oS.C,oS.C+oS.alphas[j]-oS.alphas[i] )
		else:
			L=max(0,oS.alphas[i]+oS.alphas[j]-oS.C)
			H=min(oS.C,oS.alphas[i]+oS.alphas[j] )
		if L==H:
			print("L==H")
			return 0			
		#eta = 2.0*oS.X[i,:]*oS.X[j,:].T-oS.X[i,:]*oS.X[i,:].T-\
		#	oS.X[j,:]*oS.X[j,:].T
		eta=2.0*oS.K[i,j]-oS.K[i,i]-oS.K[j,j]		
		if eta >=0: 
			print("eta>=0")
			return 0
		#求得alpha2	
		oS.alphas[j]-=oS.labelMat[j]*(Ei-Ej)/eta
		oS.alphas[j]=clipAlpha(oS.alphas[j],H,L)
		#只要修改alpha和b的值就应该更新Ek
		updateEk(oS,j) #更新误差缓存
		if abs(oS.alphas[j]-alphaJold)<0.00001:
			print('j not moving enought')
			return 0
		#求得alpha1	
		oS.alphas[i]+=oS.labelMat[j]*oS.labelMat[i]*(alphaJold-oS.alphas[j])
		updateEk(oS,i) #更新误差缓存
		#更新b1,b2-->b
		#b1=oS.b-Ei-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*\
		#	(oS.X[i,:]*oS.X[i,:].T)-oS.labelMat[j]*(oS.alphas[j]-alphaJold)*\
		#	(oS.X[j,:]*oS.X[i,:].T)
		#b2=oS.b-Ej-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*\
		#	(oS.X[i,:]*oS.X[j,:].T)-oS.labelMat[j]*(oS.alphas[j]-alphaJold)*\
		#	(oS.X[j,:]*oS.X[j,:].T)
		b1=oS.b-Ei-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.K[i,i]-\
					oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.K[j,i]
		b2=oS.b-Ej-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.K[i,j]-\
					oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.K[j,j]
		
		if oS.alphas[i]>0 and oS.alphas[i]<oS.C: oS.b=b1
		elif oS.alphas[j]>0 and oS.alphas[j]<oS.C: oS.b=b2
		else: oS.b = (b1+b2)/2.0

		return 1
	else:
		return 0
			
			
#完整版Platt SMO的外循环代码
def smoP(dataMatIn,classLabels,C,toler,maxIter,kTup=('line',0)):
	"""Platt SMO代码-->包括对两个变量的二次规划解析方法和每个子问题两个优化变量的启发式选择方法
	parameters:
		dataMatIn:训练样本
		classLabels:样本标签
		C:常量C
		toler: 容错量
		maxIter：最大迭代次数
	returns:
	"""
	#保存一些重要数据的对象
	oS = optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler,kTup)
	#控制函数退出的一些变量
	iterNum=0 			
	entireSet = True	
	alphaPairsChanged=0
	
	#当迭代次数超过指定的最大值，或者遍历整个集合都未对任意alpha对进行修改时，就退出循环
	while (iterNum<maxIter) and ((alphaPairsChanged>0) or(entireSet)):
		''' 该循环的目的是为了使得所有的样本点都满足KKT条件'''
		alphaPairsChanged = 0  
		if entireSet:
			#在数据集上遍历任意可能的alpha
			for i in range(oS.m):					#遍历所有的值
				alphaPairsChanged += innerL(i,oS)	
			print("fullSet,iter: %d i: %d, pairs changed %d" %(iterNum,i,alphaPairsChanged))
			iterNum+=1
		else:
			#alpha>0&&alpha<C--->yi*g(xi)=1支撑向量点
			#去支撑向量点中找寻可能的alpha
			nonBoundIs=nonzero( (oS.alphas.A>0)*(oS.alphas.A<C) )[0]
			for i in nonBoundIs:
				alphaPairsChanged+=innerL(i,oS)
				print("bound,iter: %d i: %d,pairs changed %d" %(iterNum,i,alphaPairsChanged))
			iterNum += 1
			
		if entireSet:entireSet = False
		elif alphaPairsChanged == 0 :entireSet=True #表示整个过程中都没有对任何alpha进行修改，则需要在整个数据集上进行查找
		
		print("iteration number: %d " %iterNum) 
		
	return oS.b, oS.alphas
	
#分离超平面
def calcWs(alphas,dataArr,classLabels):
	'''计算w-->g(x)=Wx+b '''
	X=mat(dataArr)
	labelMat=mat(classLabels).transpose()
	m,n=shape(X)
	#w是针对每个属性的	
	w=zeros((n,1))
	for i in range(m):
		w+=multiply(alphas[i]*labelMat[i],X[i,:].T)
	return w
	

#分类决策函数
def classifySVM(w,b,x):
	'''分类决策函数 '''
	W=mat(w)#n*1
	x=mat(x)#1*n
	f=sign(x*W+b)
	return f
		

#在测试中使用核函数
def testRbf(kf=1.3):
	dataArr,labelArr=loadDataSet('testSetRBF.txt')
	b,alphas=smoP(dataArr,labelArr,200,0.0001,10000,('rbf',kf))
	dataMat=mat(dataArr)
	labelMat=mat(labelArr).transpose()
	
	#选出支持向量
	svInd=nonzero(alphas.A>0)[0]
	sVs=dataMat[svInd]
	labelSV=labelMat[svInd]
	print('there are %d Support Vectors' %shape(sVs)[0])
	m,n=shape(dataMat)
	
	errorCount=0
	for i in range(m):
		kernelEval=kernelTrans(sVs,dataMat[i,:],('rbf',kf))
		predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b#分类决策函数
		if sign(predict)!=sign(labelArr[i]):errorCount+=1
	print('the training error rate is: %f' %(float(errorCount/m)))
	
	dataArr,labelArr=loadDataSet('testSetRBF2.txt')
	errorCount=0
	dataMat=mat(dataArr)
	labelMat=mat(labelArr).transpose()
	m,n=shape(dataMat)
	for i in range(m):
		kernelEval=kernelTrans(sVs,dataMat[i,:],('rbf',kf))
		predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
		if sign(predict)!=sign(labelArr[i]):errorCount+=1
	print('the test error rate is:%f' %(float(errorCount)/m))
	
	


#手写识别数字
def img2vector(filename):
	''' 将图像格式处理为一个向量'''
	returnVect = zeros( (1,1024) )
	try:
		with open(filename) as fr:
			for i in range(32):        #处理行
				lineStr = fr.readline  ().strip()
				for j in range(32):	   #处理列
					returnVect[0,32*i+j]=int( lineStr[j] )
	except:
		print("error! ")
	return returnVect
	
def loadImages(dirname):
	from os import listdir
	hwLabels=[]
	trainingFileList=listdir(dirname)
	m=len(trainingFileList)
	trainingMat=zeros((m,1024))
	for i in range(m):
		fileNameStr=trainingFileList[i]
		fileStr=fileNameStr.split('.')[0]
		classNumStr=int(fileStr.split('_')[0])
		#此处不太明白？？？？ SVM本质上是一个二类分类问题，类别标签为-1或者+1
		if classNumStr==9:
			hwLabels.append(-1)
		else:
			hwLabels.append(1)
		trainingMat[i,:]=img2vector('%s/%s' %(dirname,fileNameStr))
	return trainingMat,hwLabels
	
def testDigits(kTup=('rbf',10)):
	dataArr,labelArr=loadImages('trainingDigits')
	b,alphas=smoP(dataArr,labelArr,200,0.0001,10000,kTup)
	dataMat=mat(dataArr)
	labelMat=mat(labelArr).transpose()
	
	#选出支持向量
	svInd=nonzero(alphas.A>0)[0]
	sVs=dataMat[svInd]
	labelSV=labelMat[svInd]
	print('there are %d Support Vectors' %shape(sVs)[0])
	m,n=shape(dataMat)
	
	errorCount=0
	for i in range(m):
		kernelEval=kernelTrans(sVs,dataMat[i,:],kTup)
		predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b#分类决策函数
		if sign(predict)!=sign(labelArr[i]):errorCount+=1
	print('the training error rate is: %f' %(float(errorCount/m)))
	
	dataArr,labelArr=loadImages('testDigits')
	errorCount=0
	dataMat=mat(dataArr)
	labelMat=mat(labelArr).transpose()
	m,n=shape(dataMat)
	for i in range(m):
		kernelEval=kernelTrans(sVs,dataMat[i,:],kTup)
		predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
		if sign(predict)!=sign(labelArr[i]):errorCount+=1
	print('the test error rate is:%f' %(float(errorCount)/m))
	







































