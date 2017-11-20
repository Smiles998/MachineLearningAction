# coding=gbk
import bayes
'''
listOPosts,listClasses = bayes.loadDataSet()

myVocabList = bayes.createVocabList(listOPosts)

print(sorted(myVocabList))

flagLab=bayes.setOfWords2Vec(myVocabList,listOPosts[0])
print(flagLab)

#�õ���ȡ��������ĵ����Լ��ĵ����������
listOPosts,listClasses = bayes.loadDataSet()

#����һ���������дʵ��б�
myVocabList = bayes.createVocabList(listOPosts)

#���������ɵ��б�
trainMat=[]
for postinDoc in listOPosts:
	trainMat.append( bayes.setOfWords2Vec(myVocabList,postinDoc) )
	
#�õ��������ĸ������������������ĵ��ĸ���
p0V,p1V,pAb = bayes.trainNB0(trainMat,listClasses)

print(pAb)
print(p0V)
print(p1V)
'''
#�ж���վ�����Ƿ��Ƕ����
bayes.testingNB()

#���������ʼ�
errRaiosum=0.0
for i in range(10):
	errRaiosum += bayes.spamTest()

print('ƽ��������Ϊ��' +str( errRaiosum/10))
	
