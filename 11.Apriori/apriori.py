# coding=gbk



#Apriori�㷨�еĸ�������
def loadDataSet():
	'''�������� '''
	return [[1,3,4],[2,3,5],[1,2,3,5],[2,5] ]
	

def createC1(dataSet):
	'''����C1���ϣ���СΪ1�����к�ѡ��ļ���
	parameters:
		dataSet:transactions����
	'''
	C1=[]
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	#��C1��ÿ���򹹽�һ�����伯��
	#print("-----------------------")
	#print(C1)
	return list(map(frozenset,C1))
	
def scanD(D,Ck,minSupport):
	'''ɨ���D(transactions�ļ���)---->�Ӻ�ѡ���в���Ƶ���
		ɨ�����ݼ����ж���Щֻ��һ��Ԫ�ص���Ƿ�������С֧�ֶȵ�Ҫ���������Ҫ�������ɼ���L1
	��L1�е�Ԫ���໥��Ϲ���C2��C2�ٽ�һ�����˱��L2
	���ܣ��ú������ڴ�C1������L1
	parameters:
		D�����е�transactions����
		Ck:���ݼ�Ck->������ѡ����б�
		minSupport:����Ȥ�����С֧�ֶ�
	returns:
		retList:֧�ֶ�>��С֧�ֶ���ֵ���    
		supportData:��Լ���Ӧ��֧�ֶ�(֧�ֶ�>��С֧�ֶ���ֵ���)
		����Ƶ����Լ���Ӧ��֧�ֶ�
	'''
	ssCnt={}
	#��ѭ����Ϊ�˼���Ck�е�������ݿ��г��ֵ�Ƶ��
	for tid in D:#���ݿ��е�ÿһ������
		for can in Ck:#Ck�е�ÿһ���
			#��Ҫ���Ӽ�����������֮ǰ�洢��ʱ��ͱ���ʹ�ü��ϴ洢��
			#�����ֵ�ļ����Ǽ��ϣ����Լ���ʹ�õ���frozenset
			if can.issubset(tid):#�Ƿ���tid������Ӽ�
				if not can in ssCnt.keys():
					ssCnt[can]=1
				else:
					ssCnt[can]+=1
	#������ĸ���				
	numItems=float(len(D))
	#print("numItems: %f"  %numItems )
	#print("ssCnt: ")
	#print(ssCnt)
	#����֧�ֶ�>��С֧�ֶ���ֵ���
	retList=[]
	supportData={}
	for key in ssCnt:
		support=ssCnt[key]/numItems
		if support>=minSupport:
			retList.insert(0,key)#���б���ײ����������µļ���
		supportData[key]=support
	#print('-------retList------')
	return retList,supportData
			

def aprioriGen(Lk,k):
	''' ������ѡ�Ck+1--->��Ƶ���Lk�в�����ѡ�Ck+1
	parameters:
		Lk:Ƶ����б�Lk
		k���Ԫ�ظ���k��ע�⣺�����k>=2��
	returns:
		Ck+1����Ƶ���Lk�в�����ѡ�Ck+1--->���ﲢû��ʹ�ü�֦����
	'''
	retList=[]
	lenLk=len(Lk)
	#������k��в���һ��k+1�
	for i in range(lenLk):
		for j in range(i+1,lenLk):
			#print("Lk[i]:")
			#print(list(Lk[i]))
			L1=list(Lk[i])[:k-2]
			L2=list(Lk[j])[:k-2]
			L1.sort()
			L2.sort()
			#����һ��k+1�
			if L1==L2:
				retList.append(Lk[i]|Lk[j])#ʹ�ü��ϵ�union����
	'''����Ӧ�ò����֦����'''	
	#k+1Ƶ������Ӽ�k�ҲӦ����Ƶ���
	
	return retList
	    
	    
	    
	    
def apriori(dataSet,minSupport=0.5):
	'''�ú��������ɺ�ѡ����б�
	parameters:
		dataSet:���ݼ�
		minSupport:��С֧�ֶ�
	
	'''
	#���ȴ���C1��ѡ��
	C1=createC1(dataSet)
	#���ݼ�ת��Ϊ�����б�D
	D=list(map(set,dataSet))
	#����Ƶ���L1���Լ���֧�ֶ�
	L1,supportData=scanD(D,C1,minSupport)
	#L�����洢���е�Ƶ��k���k=1...��L1,L2,L3,...
	L=[L1]
	k=2
	#whileѭ�������������������Ƶ�����ֱ����һ������Ϊ��
	while(len(L[k-2])>0):
		#��k-1Ƶ�������k���ѡ��
		Ck=aprioriGen(L[k-2],k)
		#��k���ѡ������kƵ���--->�˴���û��ͨ����֦������kƵ�����k-1����Ӽ�����Ƶ�����
		Lk,supK=scanD(D,Ck,minSupport)
		#����Ƶ���
		supportData.update(supK)
		#���²�����Ƶ�����ӵ�L��
		L.append(Lk)
		k+=1
		
	return L,supportData

'''���ǵ�Ŀ���Ǽ������Ŀ��Ŷ��Լ��ҵ�������С���Ŷ�Ҫ��Ĺ���'''

#����Ƶ���֮�����Ҫ����ǿ��������
#�����������ɺ���
def generateRules(L,supportData,minConf=0.7):
	''' ����һ���������ŶȵĹ����б�
	parameters:
		L:���е�Ƶ����б�
		suportData:��һ���ֵ䣬���е�Ƶ��������Ӧ��֧�ֶ�
		minConf:��С���Ŷ���ֵ(���Ŷ�)
	returns:
	
	'''
	#���������б�
	bigRuleList=[]
	#����L�е�ÿһ��Ƶ���
	#��Ϊ�޷��ӵ�Ԫ����й���������������Ҫ�Ӱ����������߸���Ԫ�ص������ʼ���򹹽�����
	for i in range(1,len(L)):
		for freqSet in L[i]:
			#H1�ǽ�Ƶ�����ֳ��˵��������Ƶ���Ϊ{0,1,2}-->H1=[{0},{1},{2}]
			H1=[frozenset([item]) for item in freqSet]
			if i>1:#Ƶ�����Ԫ����Ŀ>2,����Ҫ��������һ���ĺϲ�,��Ҫʹ�÷ּ���(ǰ��-->����)��ǰ����٣���������
				rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
			else:#Ƶ�����Ԫ����Ŀ=2,��������Ŷ�
				calcConf(freqSet,H1,supportData,bigRuleList,minConf)
	
	return bigRuleList

#������ѡ���򼯺�
#ʹ�÷ּ���������ѡ����   
def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7):
	'''���Ԫ����Ŀ>2����в����������򣬿϶���Ҫʹ�õ��ݹ��㷨(�ϲ�������������)
	parameters:
		freqSet:��Ҫ�������������Ƶ���
		H:freqSetƵ����ĳ�����ȵ��Ӽ�����:len(H[0])=len(H[1]),...<len(freqSet)
		supportData:����Ƶ�������֧�ֶ�
		brl:�������еĹؼ����������Ŷȣ����Ŷȣ�
		minConf�����й����������С���Ŷ���ֵ
	'''
	m=len(H[0])
	if len(freqSet)>m+1:
		'''��LmƵ�������Cm+1��ѡ��'''
		Hmp1=aprioriGen(H,m+1)
		Hmp1=calcConf(freqSet,Hmp1,supportData,brl,minConf)
		if len(Hmp1)>1:
			rulesFromConseq(freqSet,Hmp1,supportData,brl,minConf)


'''���ǵ�Ŀ���Ǽ������Ŀ��Ŷ��Լ��ҵ�������С���Ŷ�Ҫ��Ĺ���'''
#�Թ����������	
def calcConf(freqSet,H,supportData,brl,minConf=0.7):
	''' �������Ŀ��Ŷ��Լ��ҵ�������С���Ŷ�Ҫ��Ĺ���
	parameters:
		freqSet:��Ҫ�������������Ƶ���
		H:����Ƶ�����ֳ��˵��������Ƶ���Ϊ{0,1,2}-->H1=[{0},{1},{2}]
		suppportData:����Ƶ�������֧�ֶ�
		br1:>��С���ŶȵĹ�������
		minConf:��С���Ŷ���ֵ
	returns:
		prunedH:����������С���Ŷ�Ҫ��Ĺ����б�
	'''
	prunedH=[]
	#����H�е������
	for conseq in H:
		#�����˴����Ŷȼ�����ǲ���-->��ʵ�˴��Ĺ�������Ϊ:freqSet-conseq===>conseq
		conf = supportData[freqSet]/supportData[freqSet-conseq]
		if conf>=minConf:
			print(freqSet-conseq,'---->',conseq,'conf:',conf)
			#brl��������freqSet-conseq--->conseq
			brl.append((freqSet-conseq,conseq,conf))
			prunedH.append(conseq)
	
	return prunedH
	
























