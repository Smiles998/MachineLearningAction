# coding=gbk
import apriori


#导入数据集
dataSet=apriori.loadDataSet()
'''
#创建第一个候选项集集合C1
C1=apriori.createC1(dataSet)
print("C1:")
print(list(C1))

#构建集合表示数据集D
D=list(map(set,dataSet))
print("D:")
print(D)

#有了集合形式的数据，就可以去掉那些不满足最小支持度的项集
L1,suppData0=apriori.scanD(D,C1,0.7)
print("L1:")
print(L1)

L,suppData=apriori.apriori(dataSet,minSupport=0.5)
print("L:")
print(L)


#得到所有的频繁项集及其对应的支持度
L,suppData=apriori.apriori(dataSet,minSupport=0.5)

rules=apriori.generateRules(L,suppData,minConf=0.5)
#print(rules)
'''

mushDataSet=[line.split() for line in open('mushroom.dat').readlines()]
L,suppData=apriori.apriori(mushDataSet,minSupport=0.3)
for item in L[3]:
	if '2' in item:
		print(item)




















