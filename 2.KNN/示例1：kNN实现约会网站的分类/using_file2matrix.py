import matplotlib
import matplotlib.pyplot as plt
from numpy import *
#设置中文字体
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']#指定默认字体
mpl.rcParams['axes.unicode_minus'] = False#解决保存图像是负号'-'显示为方格的问题

import kNN

filename = "datingTestSet2.txt"
datingDataMat,datingLabels = kNN.file2matrix(filename)

'''
print(datingDataMat)
print(datingLabels[0:20])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
plt.xlabel("玩视频游戏所耗时间百分比",fontsize=14)
plt.ylabel("每周晓飞的冰淇淋公升数",fontsize=14)

plt.show()
'''
normDataSet,ranges,minValues = kNN.autoNorm(datingDataMat)
print('normDataSet:')
print(normDataSet)
print('ranges:')
print(ranges)
print('minValues:')
print(minValues)
