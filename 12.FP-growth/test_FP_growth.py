# coding=gbk
from numpy import *

import fp_growth


'''
#创建树的一个单节点
rootNode=fp_growth.treeNode('pyramid',9,None)
#为其增加一个子节点
rootNode.children['eye']=fp_growth.treeNode('eye',13,None)

rootNode.disp()



#导入事务数据库实例
simpData=fp_growth.loadSimpData()
#print("simpData:")
#print(simpData)

#对数据进行格式化处理
initSet=fp_growth.createInitSet(simpData)
#print("initSet:")
#print(initSet)

myFPtree,myHeaderTab=fp_growth.createTree(initSet,3)

#print("myFPtree:")
#print(myFPtree)
#myFPtree.disp()

print("myFPtree:")
#print(myFPtree)
myFPtree.disp()


print("myHeaderTab:")
for item in myHeaderTab.items():
	print(item)
	
path=fp_growth.findPrefixPath('r',myHeaderTab['r'][1])
print("path:")	
print(path)

#建立一个空列表来存储所有的频繁项集
freqItems=[]
fp_growth.minTree(myFPtree,myHeaderTab,3,set([]),freqItems)


'''

parsedDat=[line.split() for line in open('kosarak.dat').readlines()]
initSet=fp_growth.createInitSet(parsedDat)
myFPtree,myHeaderTab=fp_growth.createTree(initSet,100000)
myFreqList=[]
fp_growth.minTree(myFPtree,myHeaderTab,100000,set([]),myFreqList)
print(len(myFreqList))





