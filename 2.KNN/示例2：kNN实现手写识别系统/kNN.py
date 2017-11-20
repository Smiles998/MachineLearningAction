from numpy import *
import os
import operator


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
    
    #使用欧式距离求解
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

filename='./digits/testDigits/0_0.txt'
testVect = img2vector(filename)


def handwriteingClassTest():
	hwLabels = []
	#得到训练数据的文件名称
	trainingFileList = os.listdir('./digits/trainingDigits')#os模块中listdir列出指定文件的内容的列表
	m=len(trainingFileList)
	#存储所有训练数据
	trainingMat = zeros( (m,1024) ) 
	for i in range(m):
		fileNameStr = trainingFileList[i]
		#得到文件的标签
		fileStr = fileNameStr.split('.')[0]
		classNumStr = int(fileStr.split('_')[0] )
		hwLabels.append(classNumStr)
		#将每个文件中的数字图像存储到矩阵中
		trainingMat[i,:]=img2vector('./digits/trainingDigits/%s' %fileNameStr)
		
	#得到测试数据
	testFileStr = os.listdir('./digits/testDigits')
	errorCount = 0.0
	mTest = len(testFileStr)
	for i in range(mTest):
		fileNameStr = testFileStr[i]
		fileStr = fileNameStr.split('.')[0]
		classNumStr = int(fileStr.split('_')[0])
		
		vectorUnderTest = img2vector('./digits/testDigits/%s' %fileNameStr)
		classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)
		print('the classifier came back with: %d, the real answer is :%d'
				%(classifierResult,classNumStr))
		if (classifierResult != classNumStr): errorCount +=1.0
		
	print('\nthe total number of errors is:%d' %errorCount)
	print('\nthe total error rate is: %f' %(errorCount/float(mTest)))
	
handwriteingClassTest()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
