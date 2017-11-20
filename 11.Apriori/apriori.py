# coding=gbk



#Apriori算法中的辅助函数
def loadDataSet():
	'''加载数据 '''
	return [[1,3,4],[2,3,5],[1,2,3,5],[2,5] ]
	

def createC1(dataSet):
	'''生成C1集合：大小为1的所有候选项集的集合
	parameters:
		dataSet:transactions集合
	'''
	C1=[]
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	#对C1中每个向构建一个不变集合
	#print("-----------------------")
	#print(C1)
	return list(map(frozenset,C1))
	
def scanD(D,Ck,minSupport):
	'''扫描库D(transactions的集合)---->从候选集中产生频繁项集
		扫描数据集来判断这些只有一个元素的项集是否满足最小支持度的要求，满足最低要求的项集构成集合L1
	而L1中的元素相互组合构成C2，C2再进一步过滤变成L2
	功能：该函数用于从C1中生成L1
	parameters:
		D：所有的transactions集合
		Ck:数据集Ck->包括候选项集的列表
		minSupport:感兴趣项集的最小支持度
	returns:
		retList:支持度>最小支持度阈值的项集    
		supportData:项集以及对应的支持度(支持度>最小支持度阈值的项集)
		返回频繁项集以及对应的支持度
	'''
	ssCnt={}
	#此循环是为了计算Ck中的项集在数据库中出现的频率
	for tid in D:#数据库中的每一个事务
		for can in Ck:#Ck中的每一个项集
			#是要用子集操作，所有之前存储的时候就必须使用集合存储，
			#并且字典的键就是集合，所以集合使用的是frozenset
			if can.issubset(tid):#是否是tid事务的子集
				if not can in ssCnt.keys():
					ssCnt[can]=1
				else:
					ssCnt[can]+=1
	#总事务的个数				
	numItems=float(len(D))
	#print("numItems: %f"  %numItems )
	#print("ssCnt: ")
	#print(ssCnt)
	#计算支持度>最小支持度阈值的项集
	retList=[]
	supportData={}
	for key in ssCnt:
		support=ssCnt[key]/numItems
		if support>=minSupport:
			retList.insert(0,key)#在列表的首部插入任意新的集合
		supportData[key]=support
	#print('-------retList------')
	return retList,supportData
			

def aprioriGen(Lk,k):
	''' 产生候选项集Ck+1--->从频繁项集Lk中产生候选项集Ck+1
	parameters:
		Lk:频繁项集列表Lk
		k：项集元素个数k（注意：这里的k>=2）
	returns:
		Ck+1：从频繁项集Lk中产生候选项集Ck+1--->这里并没有使用剪枝技术
	'''
	retList=[]
	lenLk=len(Lk)
	#从两个k项集中产生一个k+1项集
	for i in range(lenLk):
		for j in range(i+1,lenLk):
			#print("Lk[i]:")
			#print(list(Lk[i]))
			L1=list(Lk[i])[:k-2]
			L2=list(Lk[j])[:k-2]
			L1.sort()
			L2.sort()
			#构成一个k+1项集
			if L1==L2:
				retList.append(Lk[i]|Lk[j])#使用集合的union操作
	'''以下应该补充剪枝技术'''	
	#k+1频繁项集的子集k项集也应该是频繁项集
	
	return retList
	    
	    
	    
	    
def apriori(dataSet,minSupport=0.5):
	'''该函数会生成候选项集的列表
	parameters:
		dataSet:数据集
		minSupport:最小支持度
	
	'''
	#首先创建C1候选集
	C1=createC1(dataSet)
	#数据集转化为集合列表D
	D=list(map(set,dataSet))
	#创建频繁项集L1，以及其支持度
	L1,supportData=scanD(D,C1,minSupport)
	#L用来存储所有的频繁k项集（k=1...）L1,L2,L3,...
	L=[L1]
	k=2
	#while循环用来创建包含更大的频繁项集，直到下一个大的项集为空
	while(len(L[k-2])>0):
		#从k-1频繁项集产生k项集候选集
		Ck=aprioriGen(L[k-2],k)
		#从k项集候选集产生k频繁项集--->此处并没有通过剪枝（定理：k频繁项集的k-1项集的子集都是频繁项集）
		Lk,supK=scanD(D,Ck,minSupport)
		#保存频繁项集
		supportData.update(supK)
		#将新产生的频繁项集添加到L中
		L.append(Lk)
		k+=1
		
	return L,supportData

'''我们的目标是计算规则的可信度以及找到满足最小可信度要求的规则'''

#产生频繁项集之后就需要产生强关联规则：
#关联规则生成函数
def generateRules(L,supportData,minConf=0.7):
	''' 生成一个包含可信度的规则列表
	parameters:
		L:所有的频繁项集列表
		suportData:是一个字典，所有的频繁项集及其对应的支持度
		minConf:最小置信度阈值(可信度)
	returns:
	
	'''
	#构建规则列表
	bigRuleList=[]
	#遍历L中的每一个频繁项集
	#因为无法从单元素项集中构建关联规则，所以要从包含两个或者更多元素的相机开始规则构建过程
	for i in range(1,len(L)):
		for freqSet in L[i]:
			#H1是将频繁项集拆分成了单个项，如若频繁项集为{0,1,2}-->H1=[{0},{1},{2}]
			H1=[frozenset([item]) for item in freqSet]
			if i>1:#频繁项集的元素数目>2,则需要对其做进一步的合并,需要使用分级法(前体-->后体)：前体减少，后体增加
				rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
			else:#频繁项集的元素数目=2,计算其可信度
				calcConf(freqSet,H1,supportData,bigRuleList,minConf)
	
	return bigRuleList

#产生候选规则集合
#使用分级法产生候选规则   
def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7):
	'''从项集元素数目>2的项集中产生关联规则，肯定需要使用到递归算法(合并产生关联规则)
	parameters:
		freqSet:需要产生关联规则的频繁项集
		H:freqSet频繁项集的长度相等的子集，即:len(H[0])=len(H[1]),...<len(freqSet)
		supportData:所有频繁项集及其支持度
		brl:保存所有的关键规则及其置信度（可信度）
		minConf：所有关联规则的最小置信度阈值
	'''
	m=len(H[0])
	if len(freqSet)>m+1:
		'''由Lm频繁项集产生Cm+1候选集'''
		Hmp1=aprioriGen(H,m+1)
		Hmp1=calcConf(freqSet,Hmp1,supportData,brl,minConf)
		if len(Hmp1)>1:
			rulesFromConseq(freqSet,Hmp1,supportData,brl,minConf)


'''我们的目标是计算规则的可信度以及找到满足最小可信度要求的规则'''
#对规则进行评估	
def calcConf(freqSet,H,supportData,brl,minConf=0.7):
	''' 计算规则的可信度以及找到满足最小可信度要求的规则
	parameters:
		freqSet:需要产生关联规则的频繁项集
		H:将该频繁项集拆分成了单个项，如若频繁项集为{0,1,2}-->H1=[{0},{1},{2}]
		suppportData:所有频繁项集及其支持度
		br1:>最小可信度的关联规则
		minConf:最小可信度阈值
	returns:
		prunedH:保存满足最小可信度要求的规则列表
	'''
	prunedH=[]
	#遍历H中的所有项集
	for conseq in H:
		#？？此处置信度计算很是不解-->其实此处的关联规则为:freqSet-conseq===>conseq
		conf = supportData[freqSet]/supportData[freqSet-conseq]
		if conf>=minConf:
			print(freqSet-conseq,'---->',conseq,'conf:',conf)
			#brl关联规则freqSet-conseq--->conseq
			brl.append((freqSet-conseq,conseq,conf))
			prunedH.append(conseq)
	
	return prunedH
	
























