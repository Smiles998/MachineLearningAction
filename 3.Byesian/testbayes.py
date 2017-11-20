# coding=gbk
import bayes
import feedparser

'''
listOPosts,listClasses = bayes.loadDataSet()

myVocabList = bayes.createVocabList(listOPosts)

print(sorted(myVocabList))

flagLab=bayes.setOfWords2Vec(myVocabList,listOPosts[0])
print(flagLab)

#得到抽取特征后的文档，以及文档所属的类别
listOPosts,listClasses = bayes.loadDataSet()

#构建一个包含所有词的列表
myVocabList = bayes.createVocabList(listOPosts)

#词向量构成的列表
trainMat=[]
for postinDoc in listOPosts:
	trainMat.append( bayes.setOfWords2Vec(myVocabList,postinDoc) )
	
#得到两个类别的概率向量，和侮辱性文档的概率
p0V,p1V,pAb = bayes.trainNB0(trainMat,listClasses)

print(pAb)
print(p0V)
print(p1V)

#判断网站留言是否是恶意的
bayes.testingNB()

#过滤垃圾邮件
errRaiosum=0.0
for i in range(10):
	errRaiosum += bayes.spamTest()

print('平均错误率为：' +str( errRaiosum/10))
'''	

ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')

print(len(ny))
print(len(sf))
'''
errorRatioSum=0.0
for i in range(10):
	#vocabList,pSF,pNy=bayes.localWords(ny,sf)
	errorRatioSum+=bayes.localWords(ny,sf)
print("平均错误率："+str(errorRatioSum/10))
'''

bayes.getTopWords(ny,sf)





























