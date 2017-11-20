from numpy import *			#导入科学计算包Numpy
import operator				#运算符模块

#收集数据，准备数据
def createDataSet():
    group=array([ [1.0,1.1],[1.0,1.0],[0,0],[0,0.1]   ]) #数据
    lables=['A','A','B','B']							 #标签
    return group,lables


def classify0(inX,dataSet,labels,k):
    '''
	indx:用于分类的输入向量
	dataSet:train dataset
	label:  the labels for train dataset
	k:用于选择最近邻的数目
    '''
    #得到行数
    dataSetSize=dataSet.shape[0]#array.shape-->返回数组维度的一个tuple
    ''' 计算train data和inx之间的欧式距离'''
    #tile(A,rep)--->以res格式重复A,生成一个矩阵
    diffMat=tile(inX,(dataSetSize,1))-dataSet#矩阵减法
    sqDiffMat=diffMat**2# 符号"** "--->表示幂运算
    sqDistances=sqDiffMat.sum(axis=1)#按行求和   >sum(axis=0)表示按列求和
    distances=sqDistances**0.5
    sortedDistIndicies=distances.argsort()#返回的是排序行/列的下标
    
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1#get(key[, default]) #Return the value for key if key is in the dictionary, else default. If default is not given, it defaults to None, so that this method never raises a KeyError.


        
    sortedClassCount=sorted(classCount.items(),
                                key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]


#将文本记录转换为训练样本矩阵和类标签向量
def file2matrix(filename):
	''' 将文本记录转换为训练样本矩阵和类标签向量
	parameters:
	filename:数据文件名称
	return:训练样本矩阵和类标签向量	
	'''
	try:
		with open(filename) as fr:
			arrayOLines = fr.readlines()#将文本中的所有数据行都读取进来,以列表形式进行存储，每一行数据为列表的一个元素
	except:
		print('error:读取文件失败')
	else:
		numberOfLines = len(arrayOLines)#得到行数
		#returnMat:训练数据
		returnMat = zeros( (numberOfLines,3) )  
		classLabelVector = []
		index = 0
		for line in arrayOLines:
			line=line.strip()
			listFromLine = line.split('\t')#以‘\t’作为分隔符，并且返回一个列表 
			returnMat[index,:]=listFromLine[0:3]#存放第index行元素
			classLabelVector.append( int(listFromLine[-1]) )
			index +=1
				
		return returnMat,classLabelVector;
	

#数据归一化
def autoNorm(dataSet):
	''' 对数据进行归一化处理'''
	'''
	parameters:
		dataSet:需要进行归一化的数据
	returns:
		返回归一化后的数据，每列数据最大值和最小值的差值，每列数据的最小值
	'''
	#对数据进行按列求其min和max
	minValues = dataSet.min(0)#0表示对array进行按列操作
	maxValues = dataSet.max(0)
	ranges = maxValues - minValues;
	normDataSet = zeros(shape(dataSet))
	m=dataSet.shape[0]
	normDataSet = dataSet-tile(minValues,(m,1) )
	normDataSet = normDataSet/tile(ranges,(m,1) )
	return normDataSet,ranges,minValues
	
	
#测试分类器的性能
def datingClassTest():
	''' 分类器针对约会网站的测试代码'''
	hoRatio = 0.10
	datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
	normMat,ranges,minValues = autoNorm(datingDataMat)
	m=normMat.shape[0]#得到样本总数
	numTestVecs = int(m*hoRatio)#得到测试样本数
	errorCount = 0.0
	for i in range(numTestVecs):#测试样本取得为前10%
		classifierResult = classify0( normMat[i,:],
			normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3 )
		print("the classifier came back with: %d,the real answer is:%d"
				%(classifierResult,datingLabels[i]))
		
		if(classifierResult != datingLabels[i]):
			errorCount += 1.0
		
	print("the total error rate is: %f" %(errorCount/float(numTestVecs)))
		
#datingClassTest()


#使用算法：构建完整可用系统
def classfiyPerson():
	'''约会网站测试函数'''
	resultList = ['not at all' , 'in small doses', 'in large doses']
	percentTats = float( input("percentage of time spent playing video games?"))
	ffMiles = float( input( 'frequent fliter miles earned per year?') )
	iceCream = float( input("liters of ice cream consumed per year?") )
	#获取训练数据
	datingDataMat,datingLabels = file2matrix( "datingTEstSet2.txt" )
	#处理数据：数据进行归一化处理
	normMat,ranges,minValues = autoNorm(datingDataMat)
	#输入预测数据
	inArr =(array([ffMiles,percentTats,iceCream])-minValues)/ranges
	classifierResult = classify0(inArr, normMat, datingLabels,3 )
	
	print("You will probably like this person:%s" %resultList[classifierResult-1])
	
classfiyPerson()



















