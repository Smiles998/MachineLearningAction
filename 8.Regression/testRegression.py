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

#权重图像
#regression.plotWei()     
      
#使用线性回归预测鲍鱼的年龄
#regression.predictAbaAge()

#岭回归
#regression.testRidgeAbaLone()

#逐步前向回归
xArr,yArr=regression.loadDataSet('abalone.txt')
wsArry = regression.stageWise(xArr,yArr,0.005,1000)
print(wsArry)

fig=plt.figure(1)
ax=fig.add_subplot(111)
ax.plot(wsArry)
plt.show()


xMat=mat(xArr)
yMat=mat(yArr).T
#数据标准化
xMat=regression.regularize(xMat)
yMat -= mean(yMat,0)

weights=regression.standRegres(xMat,yMat.T)
print(weights)








