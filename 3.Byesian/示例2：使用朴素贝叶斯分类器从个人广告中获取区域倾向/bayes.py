from numpy import*
import re

#词表到向量的转换函数
def loadDataSet():
	postingList=[
		['my', 'dog','has','flea','problems','help','please'],
		['maybe','not','take','him','to','dog','park','stupid'],
		['my','dalmation','is','so','cute','I','love','him'],
		['stop','posting','stupid','worthless','garbage'],
		['mr','licks','ate','my','steak','how','to','stop','him'],
		['quit','buying','worthless','dog','food','stupid' ]
	]
	
	classVec=[0,1,0,1,0,1]#1代表侮辱性文字，0代表正常言论
	return postingList,classVec


def createVocabList(dataSet):
	'''获得词汇列表--->包含在所有文档中出现的不重复词的列表 '''
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)
	
#词集模型：每个词的出现与否作为一个特征
def setOfWords2Vec(vocabList,inputSet):
	''' 
	parameters:
		vocabList:词汇表
		inputSet:某个文档
	returns:
		returnVec:文档向量，向量的每一个元素为1或0，
				  分别表示词汇表中的单词在输入文档中是否出现
	
	'''
	returnVec = [0]*len(vocabList) #创建一个所含元素全为0的向量
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print("the word:%s is not in my Vocabulary!" %word)
	return returnVec

#如果一个词在文档中出现不止一次，这可能以为中包含该词是否出现在文档中不能表达某种信息-->词袋模型
#在词袋中，每个单词可以出现多次
def bagOfWord2Vec(vocabList,inputSet):
	returnVec=[0]*len(vocabList)  
	for word in inputSet:
		if word in vocabList:
			rturnVector[vocabList.index(word)] +=1
	return returnVec;



	
#训练朴素贝叶斯分类器函数
def trainNB0(trainMatrix,trainCategory):
	''' 朴素贝叶斯分类器训练函数
	parameters:
		trainMatrix:文档矩阵
		trainCategory:每篇文档类别标签所构成的向量
	returns:
		p(wi|c1),p(wi|c0),p(c1)--->返回的概率:两个类别的概率向量，以及侮辱性文档的概率
	'''
	#训练样本个数
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	#侮辱性言论的概率p(c1) (class=1)
	pAbusive = sum(trainCategory)/float(numTrainDocs)
	#此处由于是二分类问题，因此p(0)=1-p(1)--->对于多分类问题，这个地方需要计算出各种类别的概率
 	#此处避免条件概率为0
	p0Num = ones(numWords)
	p1Num = ones(numWords)
	p0Denom = 2.0
	p1Denom = 2.0
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num +=trainMatrix[i]
			p1Denom +=sum(trainMatrix[i])
		else:
			p0Num +=trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	#采用求对数可以避免下溢，虽然他们取值不同，但是不影响最终结果
	p1Vect = log(p1Num/p1Denom)   #使用的是numpy中的log函数，可对整个向量进行求解
	p0Vect = log(p0Num/p0Denom)
	return p0Vect,p1Vect,pAbusive
	
#朴素贝叶斯分类函数
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
	''' 朴素贝叶斯分类函数  --->参数采用的numpy数组来进行计算的
	parameters:
		vec2Classify:需要分类的文档向量
		p0Vec: p(wi|c0)  ---->两个分类的条件概率
		p1Vec: p(wi|c1)
		pClass1:p(c1)  ---->先验概率
	'''
	p1=sum(vec2Classify*p1Vec)+log(pClass1)
	p0=sum(vec2Classify*p0Vec)+log(1.0-pClass1)
	if p1>p0:
		return 1
	else:
		return 0
	
	
def testingNB():
	'''测试函数
	--->封装了使用Bayes分类器模型
	'''
	listOPosts,listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat=[]
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList,postinDoc) )
	
	p0V,p1V,pAb=trainNB0(array(trainMat),array(listClasses) )
	#以上通过训练过程得到其贝叶斯分类模型
	#下面则需要对其进行测试
	testEntry = ['love','my','dalmation']
	thisDoc=array( setOfWords2Vec(myVocabList,testEntry) )
	print(str(testEntry)+" can be classified as:",end='')
	print(classifyNB(thisDoc,p0V,p1V,pAb))
	
	testEntry = ['stupid','garbage']
	thisDoc=array( setOfWords2Vec(myVocabList,testEntry) )
	print(str(testEntry)+" can be classified as:",end='')
	print(classifyNB(thisDoc,p0V,p1V,pAb))
	
	
	
#文本解析
def textParse(bigString):
	''' 文本解析
	parameters:
		bigString:需要解析的一个字符串
	returns:
		返回解析之后的文本
	
	'''
	listOfTokens = re.split(r'\W*',bigString)#re.split()支持正则及多个字符切割-->分割成一个一个的单词
	return [tok.lower() for tok in listOfTokens if len(tok)>3] #取得切割后的字符长度>3的字符，并将大写转为小写

#对贝叶斯垃圾邮件分类器进行自动化处理
def spamTest():
	''' 完整的垃圾邮件测试函数	'''
	docList=[]  	#文档列表---->每个文档以列表形式存储
	classList=[]	#类别列表
	fullText=[]		#文档内容---->所有文档内容直接添加进去
	#文件夹中共有26个文件，文件名称为1-25.txt
	for i in range(1,26):
		#spam邮件
		wordList = textParse( open('./email/spam/%d.txt' %i).read() )
		docList.append(wordList) 
		fullText.extend(wordList)
		classList.append(1)
		
		#ham邮件
		wordList = textParse(open('./email/ham/%d.txt' %i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	
	vocabList = createVocabList(docList)#创建词集
		
	trainingSet=list(range(50))  #训练集合
	testSet=[]				#测试集合
	#从训练样本中随机抽取10个样本作为测试样本
	for i in range(10):
		#random.uniform()--->产生一个服从均匀分布的样本
		randIndex=int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del trainingSet[randIndex]
	#剩下的40个样本为训练样本
	trainMat=[]
	trainClasses=[]
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
		trainClasses.append(classList[docIndex])
		
	#训练之后得到的贝叶斯分类模型
	p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
	errorCount=0
		
	#使用测试样本对其进行测试
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList,docList[docIndex])
		if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
			errorCount+=1
			#print(docList[docIndex])
			
	print('the error rate is: ',float(errorCount)/len(testSet))
	return float(errorCount)/len(testSet)
	

#RSS源分类器及高频词去除函数
def calcMostFreq(vocabList,fullText):
	import operator
	freqDict={}
	for token in vocabList:
		freqDict[token]=fullText.count(token)
	sortedFreq = sorted(freqDict.items(),key=operator.itemgetter(1),reverse=True )#降序排序
	return sortedFreq[:30]
	
def localWords(feed1,feed0):
	''' 
	parameters:
		feed1:RSS源1
		feed0:RSS源2
	return:
		vocabList: 词汇表
		p0V:		类别0的先验概率
		p1V:		类别1的先验概率
	'''
	import feedparser		#使用feedparse模块解析RSS
	docList=[]			#所有文档列表（元素为列表）
	classList=[]		#类别标签列表
	fullText=[]			#所有文档内容-->元素为字符串
	minLen = min(len(feed1['entries']), len(feed0['entries']))
	
	for i in range(minLen):
		wordList = textParse(feed1['entries'][i]['summary'])#得到文本内容
		docList.append(wordList) 							#添加到文档列表中
		fullText.extend(wordList) 							#添加到文档内容列表中
		classList.append(1)
		
		wordList=textParse(feed0['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	
	vocabList=createVocabList(docList)
	top30Words = calcMostFreq(vocabList,fullText)#得到高频的前30个词
	#将高频词语从vocabList中移除
	for pairW in top30Words:
		if pairW[0] in vocabList:
			vocabList.remove(pairW[0])
	
	#训练集，测试集进行交叉验证
	trainingSet=range(2*minLen)
	testSet=[]
	for i in range(10):#选择20个测试样本
		randIndex = int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del trainingSet[randIndex]
	
	trainMat=[]
	trainClasses=[]
	for docIndex in trainingSet:
		trainMat.append(bagOfWord2Vec(vocabList,docList[docIndex]))
		trainClasses.append(classList[docIndex])
		
	p0V,p1V,pSpam=trainNB0(array(trainMat),array(trainClasses))
	
	errorCount = 0
	for docIndex in testSet:
		wordVector = bagOfWord2Vec(vocabList,docList[docIndex])
		if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
			errorCount +=1
	print("the error rate is: ",float(errorCount)/len(testSet))
	
	return vocabList,p0V,p1V
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
