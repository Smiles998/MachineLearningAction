# coding=gbk
import svmMLiA
import datetime
import time

'''
#��ʼʱ��
starttime = time.clock()

dataArr,labelArr=svmMLiA.loadDataSet('testSet.txt')
#print(labelArr)

b,alphas=svmMLiA.smoSimple(dataArr,labelArr,0.6,0.001,40)
#print(b)
#print(alphas[alphas>0])

#����ʱ��
endtime = time.clock()
print( (endtime-starttime) )

#��ʼʱ��
starttime = time.clock()
dataArr,labelArr=svmMLiA.loadDataSet('testSet.txt')
#������볬ƽ��
b,alphas=svmMLiA.smoP(dataArr,labelArr,0.6,0.001,40)
ws=svmMLiA.calcWs(alphas,dataArr,labelArr)
#������ߺ���
lf=svmMLiA.classifySVM(ws,b,dataArr[0])
print( lf )

#����ʱ��
endtime = time.clock()
print( (endtime-starttime) )

#����svm
svmMLiA.testRbf(0.1)
'''

svmMLiA.testDigits(kTup=('rbf',20))

















