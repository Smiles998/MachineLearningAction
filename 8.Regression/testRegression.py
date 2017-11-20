#coding=gbk
from numpy import *
import matplotlib.pyplot as plt

import regression

#regression.standRegresPlot()

#regression.lwlrPlot()

'''
xArr,yArr=regression.loadDataSet('ex0.txt')
print(yArr[0])

print(regression.lwlr(xArr[0],xArr,yArr,0.001))
'''

#Ȩ��ͼ��
#regression.plotWei()     
      
#ʹ�����Իع�Ԥ�Ⱬ�������
#regression.predictAbaAge()

#��ع�
#regression.testRidgeAbaLone()

#��ǰ��ع�
xArr,yArr=regression.loadDataSet('abalone.txt')
wsArry = regression.stageWise(xArr,yArr,0.005,1000)
print(wsArry)

fig=plt.figure(1)
ax=fig.add_subplot(111)
ax.plot(wsArry)
plt.show()


xMat=mat(xArr)
yMat=mat(yArr).T
#���ݱ�׼��
xMat=regression.regularize(xMat)
yMat -= mean(yMat,0)

weights=regression.standRegres(xMat,yMat.T)
print(weights)








