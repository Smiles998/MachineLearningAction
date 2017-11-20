'''SVD算法实现和应用 '''
from numpy import*
from numpy import linalg as la


def loadExData():
	return [[1,1,1,0,0],
			[2,2,2,0,0],
			[1,1,1,0,0],
			[5,5,5,0,0],
			[1,1,0,2,2],
			[0,0,0,3,3],
			[0,0,0,1,1]]


def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

#度量相似度的各种方法
#欧氏距离相似度
def ecludSim(inA,inB):
	''' 欧氏距离相似度
	parameters:
		inA:向量A
		inB:向量B
	returns:
		相似度=1/（1+距离）
	'''
	return 1.0/(1.0+la.norm(inA-inB))

#皮尔逊相关系数相似度
def pearsSim(inA,inB):
	'''皮尔逊相关系数:由函数corrcoef()计算-->[-1,1]
	相比于欧式距离的优势在于：它对用户评级的量级并不敏感
		在该函数中需要将其进行归一化:0.5+0.5*corrcoef()
	parameters:
		inA:向量A
		inB:向量B
	returns:
		返回归一化之后的皮尔逊相关系数
	'''
	if len(inA)<3:return 1.0
	return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1]
	

#余弦相似度：计算两个向量之间夹角的余弦值
#如果夹角为90度，则相似度为0，如果两个两个向量的方向相同，则相似度为1.0
def cosSim(inA,inB):
	'''余弦相似度:由余弦公式进行计算-->[-1,1]
	归一化：0.5+0.5*cos(A,B)	
	parameters:
		inA:向量A
		inB:向量B
	returns:
		返回归一化之后的余弦相似度
	'''
	num=float(inA.T*inB)
	denom=la.norm(inA)*la.norm(inB)
	return 0.5+0.5*(num/denom)

	
#基于物品相似度的推荐引擎
def standEst(dataMat,user,simMeas,item):
	''' 用来计算在给定相似度计算方法的条件下，用户对物品的估计评分值、
	 。找到指定用户已评价过的商品与未评价过的商品之间的相似度
	parameters:
		dataMat:数据集(数据矩阵)--->行对应用户，列对应物品
		user:用户编号
		simMeas:相似度的计算方法
		item:物品编号-->该用户没有评价过得商品
	returns:
	
	'''
	#数据集中物品数目
	n=shape(dataMat)[1]
	#用于计算估计评分值的变量
	simTotal=0.0 #相似度总和
	ratSimTotal=0.0#用户级别相似度总和：相似度*用户级别
	
	#遍历行中的每个物品
	for j in range(n):
		#用户对某个物品的评分值
		userRating=dataMat[user,j] 
		
		#如果某个物品评分值为0，就意味着用户没有对该物品进行评分
		if userRating==0:
			continue
		
		#两个物品当中已经被评分的那个元素-->已经被评分的两种物品之间的相似度
		overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]
		
		if len(overLap)==0:
			#如果没有任何重合元素，则相似度为0，且终止本次循环
			similarity=0
			continue
		else:
			#基于重合物品计算相似度--->计算其他用户对两种商品评分之间的相似度
			similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])
		
		#总体相似度
		simTotal+=similarity
		ratSimTotal+=similarity*userRating#相似度与当前用户评分的乘积
		
	if simTotal==0:
		return 0
	else:
		return ratSimTotal/simTotal #这些评分值则用于对预测值进行排序
	
def recommend(dataMat,user,N=3,simMeas=cosSim,estMethod=standEst):
	''' 推荐引擎：产生最高N个推荐结果
	parameters:
		dataMat:数据集
		user:用户编号
		N:最高N个推荐结果，默认为3
		simMeas:相似度计算方法
		estMethod: 估计评分方法
	returns:	
	
	'''
	#找出该用户未评价过的商品
	unratedItems=nonzero(dataMat[user,:].A==0)[1]
	
	if len(unratedItems)==0:
		#如果所有的商品都评价过，则返回
		return "you rated everything"
	
	#在所有未评分的物品列表上进行循环
	itemScores=[]
	for item in unratedItems:
		#该用户未评价过的商品与已经该用户已评价过的商品之间的相似度估计
		estimatedScores=estMethod(dataMat,user,simMeas,item)
		itemScores.append((item,estimatedScores))
	
	#print("itemScores:")
	#print(itemScores)
	return sorted(itemScores,key=lambda jj:jj[1],reverse=True)[:N]
	
	
	
def svdEst(dataMat,user,simMeas,item):
	'''对给定用户给定物品构建一个评分估计值
	parameters:
		dataMat:数据集
		user:给定用户编号
		simMeas:相似度计算方法
		item:给定商品编号--->对该用户针对该商品构建一个评分估计值
	returns：
		返回对给定用户给定物品构建的一个评分估计值
	'''
	n=shape(dataMat)[1]
	
	simTotal=0.0
	ratSimTotal=0.0
	#对该数据集进行svd分解
	U,Sigma,VT=la.svd(dataMat)
	#只利用包含了90%能量值的奇异值
	Sig4=mat(eye(4)*Sigma[:4])
	
	#将物品转换到低维空间-->转换这个过程很是有疑问？？？
	xformedItems=dataMat.T*U[:,:4]*Sig4.T
	
	for j in range(n):
		userRating=dataMat[user,j]
		if userRating==0 or j==item:
			continue
			
		#这里的相似度计算是在低维空间中进行的?????
		similarity=simMeas(xformedItems[item,:].T,xformedItems[j,:].T)
		print("the %d and %d similarity is: %f" %(item,j,similarity))
		simTotal+=similarity
		ratSimTotal+=similarity*userRating
	
	if simTotal==0:
		return 0
	else:
		return ratSimTotal/simTotal
	
	
#基于SVD的图像压缩-->使用ＳＶＤ对数据降维，从而实现图像的压缩
def printMat(inMat,thresh=0.8):
	''' 将数字图像打印出来：>thresh=1,else =0
	parameters:
		inMat:数字图像矩阵
		thresh:打印阈值	
	'''
	for i in range(32):
		for k in range(32):
			if float(inMat[i,k])>thresh:
				print(1,end='') 
			else:
				print(0,end='')
		print()
		

def imgCompress(numSV=3,thresh=0.8):
	'''进行数字图像的压缩
	parameters:
		numSV:压缩的维数
		thresh:输出数字图像的阈值,调用printMat中所使用的参数
	
	
	'''
	myl=[]
	with open('0_5.txt') as fr:
		for line in fr.readlines():
			newRow=[]
			for i in range(32):
				newRow.append(int(line[i]))
			myl.append(newRow)
			
	myMat=mat(myl)
	print("original matrix:")
	printMat(myMat,thresh)
	
	#进行SVD分解
	U,Sigma,VT=la.svd(myMat)
	SigRecon=eye(numSV)*Sigma[:numSV]
	'''
	SigRecon=mat(zeros((numSV,numSV)))
	for k in range(numSV):
		SigRecon[k,k]=Sigma[k]
	这段代码可用上一句代码进行替换
	'''	
	reconMat=U[:,:numSV]*SigRecon*VT[:numSV,:]
	print("reconstructed matrix using %d singular values:" %numSV)
	print(reconMat,thresh)
			
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
