# coding=gbk
from numpy import*
import matplotlib.pyplot as plt

import pca

'''
#PCA测试
dataMat=pca.loadDataSet('testSet.txt')
lowDMat,reconMat=pca.pca(dataMat,2)
print(shape(lowDMat))

fig=plt.figure()
ax=fig.add_subplot(111)
ax.scatter(dataMat[:,0].flatten().A[0],dataMat[:,1].flatten().A[0],marker='^',s=90)
ax.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red')
plt.show()

'''

dataMat=pca.replaceNanWithMean()

meanVals=mean(dataMat,axis=0)
meanRemoved=dataMat-meanVals
covMat=cov(meanRemoved,rowvar=0)


























