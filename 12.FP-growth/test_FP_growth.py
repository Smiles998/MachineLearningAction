# coding=gbk
from numpy import *

import fp_growth


'''
#��������һ�����ڵ�
rootNode=fp_growth.treeNode('pyramid',9,None)
#Ϊ������һ���ӽڵ�
rootNode.children['eye']=fp_growth.treeNode('eye',13,None)

rootNode.disp()



#�����������ݿ�ʵ��
simpData=fp_growth.loadSimpData()
#print("simpData:")
#print(simpData)

#�����ݽ��и�ʽ������
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

#����һ�����б����洢���е�Ƶ���
freqItems=[]
fp_growth.minTree(myFPtree,myHeaderTab,3,set([]),freqItems)


'''

parsedDat=[line.split() for line in open('kosarak.dat').readlines()]
initSet=fp_growth.createInitSet(parsedDat)
myFPtree,myHeaderTab=fp_growth.createTree(initSet,100000)
myFreqList=[]
fp_growth.minTree(myFPtree,myHeaderTab,100000,set([]),myFreqList)
print(len(myFreqList))





