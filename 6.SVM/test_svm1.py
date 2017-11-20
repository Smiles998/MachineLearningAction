# coding=gbk
import svmMLiA
import datetime
import time

'''
#开始时间
starttime = time.clock()

dataArr,labelArr=svmMLiA.loadDataSet('testSet.txt')
#print(labelArr)

b,alphas=svmMLiA.smoSimple(dataArr,labelArr,0.6,0.001,40)
#print(b)
#print(alphas[alphas>0])

#结束时间
endtime = time.clock()
print( (endtime-starttime) )

#开始时间
starttime = time.clock()
dataArr,labelArr=svmMLiA.loadDataSet('testSet.txt')
#求出分离超平面
b,alphas=svmMLiA.smoP(dataArr,labelArr,0.6,0.001,40)
ws=svmMLiA.calcWs(alphas,dataArr,labelArr)
#分类决策函数
lf=svmMLiA.classifySVM(ws,b,dataArr[0])
print( lf )

#结束时间
endtime = time.clock()
print( (endtime-starttime) )

#测试svm
svmMLiA.testRbf(0.1)
'''

svmMLiA.testDigits(kTup=('rbf',20))

















