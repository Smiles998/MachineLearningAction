# coding=gbk
import apriori


#�������ݼ�
dataSet=apriori.loadDataSet()
'''
#������һ����ѡ�����C1
C1=apriori.createC1(dataSet)
print("C1:")
print(list(C1))

#�������ϱ�ʾ���ݼ�D
D=list(map(set,dataSet))
print("D:")
print(D)

#���˼�����ʽ�����ݣ��Ϳ���ȥ����Щ��������С֧�ֶȵ��
L1,suppData0=apriori.scanD(D,C1,0.7)
print("L1:")
print(L1)

L,suppData=apriori.apriori(dataSet,minSupport=0.5)
print("L:")
print(L)


#�õ����е�Ƶ��������Ӧ��֧�ֶ�
L,suppData=apriori.apriori(dataSet,minSupport=0.5)

rules=apriori.generateRules(L,suppData,minConf=0.5)
#print(rules)
'''

mushDataSet=[line.split() for line in open('mushroom.dat').readlines()]
L,suppData=apriori.apriori(mushDataSet,minSupport=0.3)
for item in L[3]:
	if '2' in item:
		print(item)




















