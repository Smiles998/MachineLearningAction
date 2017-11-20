#coding=gbk
from numpy import*
import matplotlib.pyplot as plt

import kMeans

#dataMat=mat(kMeans.loadDataSet('testSet.txt'))
'''
测试加载数据，以及随机选择k个聚类中心
min0=min(dataMat[:,0])
print(min0)
max0=max(dataMat[:,0])
print(max0)

min1=min(dataMat[:,1])
print(min1)
max1=max(dataMat[:,1])
print(max1)

kmat=kMeans.randCent(dataMat,2)
print(kmat)

di=kMeans.distEclud(dataMat[0],dataMat[1])
print(di)

#测试K-Means聚类算法
myCentroids,clusterAssing=kMeans.kMeans(dataMat,4)
#print(myCentroids)

fig=plt.figure(1)
ax=fig.add_subplot(111)

#ax.scatter(list(dataMat[:,0].T),list(dataMat[:,1].T))
cluster0data = dataMat[ nonzero(clusterAssing[:,0]==0)[0] ]
cluster1data = dataMat[ nonzero(clusterAssing[:,0]==1)[0] ]
cluster2data = dataMat[ nonzero(clusterAssing[:,0]==2)[0] ]
cluster3data = dataMat[ nonzero(clusterAssing[:,0]==3)[0] ]
ax.scatter(list(cluster0data[:,0].T),list(cluster0data[:,1].T),marker='o',c='yellow')
ax.scatter(list(cluster1data[:,0].T),list(cluster1data[:,1].T),marker='*',c='green')
ax.scatter(list(cluster2data[:,0].T),list(cluster2data[:,1].T),marker='^',c='blue')
ax.scatter(list(cluster3data[:,0].T),list(cluster3data[:,1].T),marker='x',c='purple')
	
ax.scatter(list(myCentroids[:,0].T),list(myCentroids[:,1].T),c='red',marker='+')
plt.show()


print("--------------------")
print(clusterAssing)
'''


#测试二分K-Means聚类算法
dataMat3=mat(kMeans.loadDataSet('testSet2.txt'))
centList,myNewAssments=kMeans.biKmeans(dataMat3,3)


fig=plt.figure(1)
ax=fig.add_subplot(111)

#ax.scatter(list(dataMat[:,0].T),list(dataMat[:,1].T))
cluster0data = dataMat3[ nonzero(myNewAssments[:,0]==0)[0] ]
cluster1data = dataMat3[ nonzero(myNewAssments[:,0]==1)[0] ]
cluster2data = dataMat3[ nonzero(myNewAssments[:,0]==2)[0] ]

ax.scatter(list(cluster0data[:,0].T),list(cluster0data[:,1].T),marker='o',c='yellow')
ax.scatter(list(cluster1data[:,0].T),list(cluster1data[:,1].T),marker='*',c='green')
ax.scatter(list(cluster2data[:,0].T),list(cluster2data[:,1].T),marker='^',c='blue')

	
ax.scatter(list(centList[:,0].T),list(centList[:,1].T),c='red',marker='+')
plt.show()


print("--------------------------------------------------")
print("type:"+str(type(centList)))
print(centList)
















