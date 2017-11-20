# coding = gbk
from numpy import*



#K-均值聚类支持函数

def loadDataSet(filename):
	''' 加载数据--->将文本文件中的数据导入到一个列表中
	parameters:
		filename:文件名称
	returns:
		dataMat:数据	（浮点数类型）
				该返回值的格式为一个包含许多其他列表的列表，这种格式很容易将很多值封装到矩阵中
	'''
	dataMat=[]
	with open(filename) as fr:
		for line in fr.readlines():
			curLine=line.strip().split('\t')
			fltLine=list(map(float,curLine))#将数值型转换为浮点数，记住外层的list必须要加上的
			dataMat.append(fltLine)
	return dataMat
	
#采用欧氏距离作为两点之间的距离度量	
def distEclud(vecA,vecB):
	''' 计算两点之间的距离--->欧式距离
	parameters:
		vecA:点A
		vecB:点B
	returns:
		A与B之间的欧氏距离
	'''
	return sqrt(sum(power(vecA-vecB,2)))
	

def randCent(dataSet,k):
	'''随机选择K个聚类中心：
		其实此时找到的随机点并不是该数据集中的点，只是这些点是在整个数据集的边界之内的点
	parameters:
		dataSet:数据集
		k：聚类的个数
	'''
	n=shape(dataSet)[1]
	centroids=mat(zeros((k,n)))
	for j in range(n):
		minJ=min(dataSet[:,j])
		rangeJ=float(max(dataSet[:,j])-minJ)
		centroids[:,j]=minJ+rangeJ*random.rand(k,1)
	return centroids


#完整的K-均值聚类算法
def kMeans(dataSet,k,distMeas=distEclud,createCent=randCent):
	'''K-均值聚类算法
	parameters:
		dataSet:数据集
		K：k个聚类中心
		distMeas:距离计算函数（距离计算方式）
		createCent:k个聚类中心的随机初始化
	returns:
		centroids：k个聚类中心
		clusterAssment：每个样本属于的聚类中心以及到聚类中心的误差
				：[聚类中心坐标，误差]
	'''
	#样本数
	m=shape(dataSet)[0]
	#每个样本点的簇分配结果：包括两列：一列记录簇索引值，第二列存储误差（当前点到簇质心的距离）
	clusterAssment=mat(zeros((m,2)))
	#聚类中心点的随机初始化
	centroids=createCent(dataSet,k)
	#每次聚类是否发生--->flag标志
	clusterChanged=True
	
	#计算质心-分配-重新计算：反复迭代，直到所有数据点的簇分配结果不再改变为止
	while clusterChanged:
		clusterChanged=False
		for i in range(m):#对于每个样本
			minDist=inf #最小距离
			minIndex=-1 #聚类下标
			#找到当前样本的聚类中心
			for j in range(k):#对于每个聚类中心
				distJI=distMeas(centroids[j,:],dataSet[i,:])
				if distJI<minDist:
					minDist=distJI
					minIndex=j
						
			#确定是否发生了聚类
			if clusterAssment[i,0]!=minIndex:
				clusterChanged=True
				clusterAssment[i,:]=[minIndex,minDist**2]
				
		#所有的样本点都已经分配到了合适的聚类中心处，此时需要重新估计聚类中心
		#print(centroids)
		for cent in range(k):
			ptsInClust=dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
			centroids[cent,:]=mean(ptsInClust,axis=0)#axis=0表示按矩阵列方向进行均值计算
			
	return centroids,clusterAssment

#二分K-均值聚类算法：
def biKmeans(dataSet,k,distMeas=distEclud):
	'''分K-均值聚类算法-->返回聚类结果
	parameters:
		dataSet:聚类的数据集
		k：聚类的簇数
		distMeas:距离计算函数
	returns:
	
	'''
	#样本数
	m=shape(dataSet)[0]
	#簇分配结果
	clusterAssment=mat(zeros((m,2)))
	#将所有点作为一个簇，找到其簇中心
	centroid0=mean(dataSet,axis=0).tolist()[0]
	#使用一个列表来保留所有的质心
	centList=[centroid0]
	print("type: " +str(type(centList)))
	for j in range(m):
		#对于每个样本点计算到聚类中心的距离平方和
		clusterAssment[j,1]=distMeas(mat(centroid0),dataSet[j,:])**2
	
	#while循环会不停地对簇进行划分，直到得到想要的簇数目为止
	while len(centList)<k:#簇个数<指定个数
		lowestSSE=inf
		#以下for循环会选择使得误差最小的簇进行划分操作
		for i in range(len(centList)):
			#当前聚类的样本
			ptsInCurrCluster=dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
			#对当前簇进行聚类(2分K-Means)
			centroidMat,splitClustAss=kMeans(ptsInCurrCluster,2,distMeas)
			#进行2分K-Means的簇的SSE
			sseSplit=sum(splitClustAss[:,1])
			#未进行二分K-Means的簇的SSE
			sseNotSplit=sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
			
			print("sseSplit=%.2f,and sseNotSplit=%.2f" %(sseSplit,sseNotSplit))
			#本次划分的误差：sseSplit+sseNotSplit
			if (sseSplit+sseNotSplit)<lowestSSE:
				bestCentToSplit=i			 	   #进行簇划分的簇索引
				bestNewCents=centroidMat.copy()	   #划分簇之后的质心，二分划分
				bestClustAss=splitClustAss.copy()  #划分簇之后的样本
				lowestSSE=sseSplit+sseNotSplit
		
		#更新分配簇的结果		
		bestClustAss[nonzero(bestClustAss[:,0].A==1)[0],0]=len(centList)
		bestClustAss[nonzero(bestClustAss[:,0].A==0)[0],0]=bestCentToSplit
		
		print("the bestCentToSplit is: %d"  %(bestCentToSplit))
		print("the len of bstClustAss is: %d" %len(bestClustAss))
		#更新质心结果
		centList[bestCentToSplit]=bestNewCents[0,:].A.tolist()[0]
		centList.append(bestNewCents[1,:].A.tolist()[0])
		#更新聚类结果
		clusterAssment[nonzero(clusterAssment[:,0].A==bestCentToSplit)[0],:]=bestClustAss
		#print("centList:")
		#print(centList)
		#print(type(centList))
	return mat(centList),clusterAssment
	
	
				
				
				
				
				
				
				
				
				
				
				
				










