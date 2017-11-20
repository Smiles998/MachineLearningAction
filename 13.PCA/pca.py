
from numpy import*

def loadDataSet(filename,delim='\t'):
	with open(filename) as fr:
		stringArr=[line.strip().split(delim) for line in fr.readlines()]
		print(shape(stringArr))
		dataArr=[ list( map(float,line) ) for line in stringArr ]
	
	return mat(list(dataArr))

def pca(dataMat,topNfeat=9999999):
	''' 使用PCA进行降维
	parameters:
		dataMat:数据集
		topNfeat:是一个可选参数，即应用的N个特征
	returns:
		lowDDataMat:原始数据通过PCA降维之后的数据
		reconMat:通过降维后的数据进行重建后的数据
	'''
	#求数据特征的均值
	meanVals=mean(dataMat,axis=0)
	#将数据减去均值--->数据中心化
	meanRemoved=dataMat-meanVals
	
	#求协方差，rowvar=True时表示将行当做一个变量，False时表示将列当做一个变量
	covMat=cov(meanRemoved,rowvar=0)
	#求协方差的特征值和特征矩阵
	eigVals,eigVects=linalg.eig(mat(covMat))
	#将所有的特征值进行排队，并返回排序后的下标--->默认是从小到大排序
	eigValInd=argsort(eigVals)
	print("eigValInd:")
	print(eigValInd)
	eigValInd=list(reversed(eigValInd))#将特征值排序的结果进行逆序-->从大到小排序
	eigValInd=eigValInd[:topNfeat]
	print("eigValInd:")
	print(eigValInd)
	#将特征向量也重新进行排序
	redEigVects=eigVects[:,eigValInd]
	#将数据与特征向量做内积--->得到降维之后的数据(从原始空间-->新空间)
	lowDDataMat=meanRemoved*redEigVects
	
	#原始数据被重构的结果
	reconMat=(lowDDataMat*redEigVects.T)+meanVals
	return lowDDataMat,reconMat


#将NaN替换成平均值的函数
def replaceNanWithMean():
	'''将NaN替换成平均值的函数 '''
	#得到数据集
	dataMat=loadDataSet('secom.data',' ')
	#得到特征数目
	numFeat=shape(dataMat)[1]
	
	for i in range(numFeat):
		#计算所有非NaN的平均值
		meanVal=mean(dataMat[nonzeros( ~isnan(dataMat[:,i].A) )[0],i ])
		#将所有NaN置为平均值
		dataMat[ nonzero(isnan(dataMat[:,i].A))[0],i ] = meanVal
		
	return dtaMat










