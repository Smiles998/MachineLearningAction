#coding=gbk
from numpy import*

def loadDataSet(filename):
	'''��������
	parameters:
		filename:�����ļ�������
	returns:
		dataMat:�õ��������б�
	'''
	dataMat=[]
	with open(filename) as fr:
		for line in fr.readlines():
			curLine=line.strip().split('\t')
			fltLine=list(map(float,curLine))#��ÿ�е����ݱ����һ�鸡����
			dataMat.append(fltLine)
			
	return dataMat


def binSplitDataSet(dataSet,feature,value):
	''' ����feature������ֵvalue�����ݼ��ֳ���������
	   �ڸ�������������ֵ������£��ú���ͨ�����ݹ��˵ķ�ʽ���������ݼ����зֵõ������Լ�������
	parameters:
		dataSet:���ݼ���
		feature:���м��ϻ��ֵ����������зֵ�������
		value:feature������ֵ
	returns:
		mat0: >value����������
		mat1: <=value����������
	'''
	mat0=dataSet[nonzero(dataSet[:,feature] > value)[0],:]
	mat1=dataSet[nonzero(dataSet[:,feature] <= value)[0],:]
	return mat0,mat1



def regLeaf(dataSet):
	''' ��������Ҷ�ڵ㣬��chooseBestSplit()����ȷ�����ٶ����ݽ����з�ʱ�������øú����õ�Ҷ�ڵ��ģ��
	�ڻع����У���ģ����ʵ����Ŀ������ľ�ֵ
	parameters:
		dataSet:���ݼ�
	returns:
		�������ݼ����һ�еľ�ֵ
	'''
	return mean(dataSet[:,-1])
	
def regErr(dataSet):
	'''�����ƺ������ú����ڸ��������ϼ���Ŀ�������ƽ�����
	parameters:
		dataSet:���ݼ�
	returns:
		�������ݼ����һ�е��ܷ���
	'''
	return var(dataSet[:,-1])*shape(dataSet)[0]
	
	
#����ĳ�������㷽�����ú������ҵ����ݼ���ѵĶ�Ԫ�зַ���
def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
	''' �ú�����Ҫ��������£�����ѷ�ʽ�з����ݼ���������Ӧ��Ҷ�ڵ�
	   �ú�����Ŀ�����ҵ����ݼ��зֵ����λ�ã����������е�����������ܵ�ȡֵ���ҵ�ʹ�����С�����з���ֵ
	parameters:
		dataSet:���ݼ�
		leafType:�ǶԴ���Ҷ�ڵ�ĺ���������
		errType���Ƕ��ܷ�����㺯����Ӧ��
		opt:��һ���û�����Ĳ������ɵ�Ԫ�飬����������Ĺ���
	returns:
		bestIndex���з�����
		bestValues���з�����ֵ
	'''		
	tolS=ops[0]#���������½�ֵ
	tolN=ops[1]#�зֵ�����������

	if len( set( dataSet[:,-1].T.tolist()[0] ) )==1:
		#�������Ŀ��ֵ������˳�������Ҷ�ڵ�
	#	print("1.���")
		return None,leafType(dataSet)
		
	m,n=shape(dataSet)
	#print("m,n: %d,%d" %(m,n))
	#�����ǰ���ݼ���Ŀ��ֵ���ܷ���
	S=errType(dataSet)
	#print("S:"+str(S))
	bestS=inf
	bestIndex=0
	bestValue=0
	
	for featIndex in range(n-1):#����ÿ������
	#	print("featIndex:%d" %featIndex)
	#	print(set(   dataSet[:,featIndex].T.tolist()[0])   )
	#	print(set(   dataSet[:,featIndex].T.tolist()[0]) )
		for splitVal in set(dataSet[:,featIndex].T.tolist()[0]):#����������ÿ��ȡֵ
			mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
			#tolN�зֵ�����������
			if(shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN):
				continue
			#�з�֮����������ݼ����ܷ���
			newS=errType(mat0)+errType(mat1)
		#	print("newS:"+str(newS))
			if (newS < bestS):
			#	print("newS<bestS")
				bestIndex=featIndex
				bestValue=splitVal
				bestS=newS
		#		print("bestS:" +str(bestS))
		#		print("bestValues:"+str(bestValue)+"\n\n")
				
	#�ܷ���� ����ܷ��tolSΪ���������½�ֵ
	if (S-bestS)<tolS: #����������˳�
	#	print("bestS: "+str(bestS))
	#	print("2.����")
	#	print(S-bestS)
		return None,leafType(dataSet)
		
	#print("bestValue:"+str(bestValue))	
	mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)

	#print(shape(mat0)[0])
	#print(shape(mat1)[0])
	if(shape(mat0)[0] < tolN) or (shape(mat1)[0]<tolN):#����зֵ����ݼ���С���˳�
	#	print("3.�зֵ����ݼ���С")
		return None,leafType(dataSet)
	#print("bestIndex:" +str(bestIndex))
	#print("bestValue:"+str(bestValue))
	return bestIndex, bestValue


#����������
def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
	'''�ݹ鹹�����Ĺ���
	parameters:
		dataSet:���ݼ�
		leafType:�����˽���Ҷ�ڵ�ĺ���
		errType: ���������㺯��
		ops:��һ��������������������������Ԫ��
	returns:
		retTree���ع��������ĸ��ڵ�root
	'''
	#ѡ����Ϊ���ʵ��з�����������ֵ
	#�������ֹͣ�������ú����᷵��None��ĳ��ģ�͵�ֵ
	#����������ǻع�������ģ����һ�������������ģ��������ģ����һ�����Է���
	feat,val=chooseBestSplit(dataSet,leafType,errType,ops)
	if feat==None:return val #Ҷ�ڵ��ֻ��һ��ֵ
	
	retTree={}
	retTree['spInd']=feat #��������
	retTree['spVal']=val  #����ֵ
	#���ݻ�������������ֵ�����ݼ�����Ϊ��������
	lSet,rSet=binSplitDataSet(dataSet,feat,val)
	#�ݹ鹹�����������������Ĺ���
	retTree['left']=createTree(lSet,leafType,errType,ops)
	retTree['right']=createTree(rSet,leafType,errType,ops)
	
	return retTree


#�ع�����֦����
def isTree(obj):
	'''�ж�����Ľڵ��Ƿ�Ϊ���ڵ��Ҷ�ڵ� ''' 
	return (type(obj).__name__=='dict')
	
	
def getMean(tree):
	'''���ظ�������������Ҷ�ڵ��ֵ�ľ�ֵ --->������ƽ��ֵ
	parameters:
		tree:��root�ڵ�
	returns��
		���ظ�������������Ҷ�ڵ��ֵ�ľ�ֵ 	
	'''
	if isTree(tree['right']):#�ж��������Ƿ�Ϊ��
		tree['right']=getMean(tree['right'])
	if isTree(tree['left']):#�ж��������Ƿ�Ϊ��
		tree['left']=getMean(tree['left'])
	#������������Ҷ�ڵ�ľ�ֵ
	return (tree['left']+tree['right'])/2.0

#��֦����
def prune(tree,testData):
	'''���ļ�֦����
		ʹ�ú��֦������Ҫ�����ݼ��ֳɲ��Լ���ѵ����������ָ��������ʹ�ù����������㹻��
	�㹻���ӣ����ڼ�֦�����������϶����ҵ�Ҷ�ڵ㣬�ò��Լ����жϽ���ЩҶ�ڵ�ϲ��Ƿ��ܼ���
	����������ǵĻ��ͺϲ�
	--���ּ�֦�����롶ͳ��ѧϰ�������������Ĳ�����ͬ
	parameters:
		tree:����֦����
		testData:��֦����Ĳ�������
	returns:
	
	'''
	#�޲�������������ݽ������ݴ���
	if shape(testData)[0]==0:
		return getMean(tree)
	#��Ϊ������ѵ�������ɵģ����Բ��Լ��ϻ���һЩ������ԭ���ݼ���ȡֵ��Χ��ͬ
	if (isTree(tree['right'])) or isTree(tree['left']):
		#����������������Բ������ݼ����л���
		lSet,rSEt=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
	if isTree(tree['left']):
		#�ݹ��֦������
		tree['left']=prune(tree['left',lSet])
	if isTree(tree['right']):
		#�ݹ��֦������
		tree['right']=prun(tree['right'],rSet)
		
	#�ڶ�����������֧��ɼ�֦֮�󣬻���Ҫ��������Ƿ���Ȼ������
	if not isTree(tree['left']) and not isTree(tree['right']):
		#����������������Ҫ���кϲ�
		lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
		#δ�ϲ������
		errorNoMerge=sum(power(lSet[:,-1]-tree['left'],2))+\
						sum(power(rSet[:,-1]-tree['right'],2))
		treeMean=(tree['left']+tree['right'])/2.0
		#�ϲ�֮������
		errorMerge=sum(power(testData[:,-1]-treeMean,2))
		if errorMerge<errorNoMerge:
			#�ϲ�֮������С����ϲ���
			print("merging")
			return treeMean  #��ΪҶ�ڵ�
		else:
			#����ֱ�ӷ��أ���������кϲ�
			return tree
	else: 
		return tree   
		
#ģ�����Ĺ���	
'''���ö�Ԫ�з֣�����ģ����--->Ҷ�ڵ㲻���Ǽ򵥵���ֵ��ȡ����֮����һЩ����ģ�� '''	
#ģ������Ҷ�ڵ����ɺ���--->���ɵ�һ������ģ��
def linearSolve(dataSet):
	'''�����ݼ���ʽ����Ŀ��������Ա���������ִ�м򵥵����Իع�
	parameters:
		dataSet:���ݼ�
	returns:
		ws:�ع�ϵ��
		X:�Ա���
		Y:Ŀ�����
	'''
	m,n=shape(dataSet)
	X=mat(ones((m,n)))
	Y=mat(ones((m,1)))
	X[:,1:n]=dataSet[:,0:n-1]
	Y=dataSet[:,-1]
	xTx=X.T*X
	#������治����Ҳ����ɳ����쳣
	if linalg.det(xTx)==0.0:
		raise NameError("This matrix is singular,cannot do inverse.\n\
						try increasing the second value of ops")
	ws=xTx.I*(X.T*Y)
	return ws,X,Y
	
def modelLeaf(dataSet):
	''' ������ݵı�׼�ع�ϵ��
	�����ݲ�����Ҫ�зֵ�ʱ��������Ҷ�ڵ��ģ��
	parameters:
		dataSet:���ݼ�
	returns:
		ws����׼�ع�ϵ��
	'''
	ws,X,Y=linearSolve(dataSet)
	return ws
	
def modelErr(dataSet):
	''' ʹ�����Իع�ó��ع�ģ�ͣ�������Ԥ��ֵ����ʵֵ֮������
	parameters:
		dataSet:���ݼ�
	returns:
		�ع�ģ�͵�Ԥ��ֵ����ʵֵ֮���ƽ������
	
	'''
	ws,X,Y=linearSolve(dataSet)
	yHat=X*ws
	return sum(power(Y-yHat,2))


#�����ع����Ԥ��Ĵ���
def regTreeEval(model,inDat):
	'''�ع��� --->�����Ҷ�ڵ㴦Ϊһ����ֵ
	'''
	return float(model)

def modelTreeEval(model,inDat):
	'''ģ���� 
		�����Ҷ�ڵ㴦��һ���ع�ģ��
	parameters:
		model:�ع�ģ��--->��ϵĻع�ϵ��
		inDat:��������
	returns:
		���ػع�ģ��Ԥ�������
	'''
	n=shape(inDat)[1] #������
	X=mat(ones((1,n+1)))
	X[:,1:n+1]=inDat
	return float(X*model)#����Ԥ��Ľ��

#�ع�����ģ������Ԥ��	
def treeForeCast(tree,inData,modelEval=regTreeEval):
	'''�ع�����ģ������Ԥ��---->�Զ����±�����������ֱ������Ҷ�ڵ�Ϊֹ
	parameters:
		tree:ѵ���õĻع�����ģ����
		inData:��������
		modelEval:��������-->����Ԥ��ķ�ʽ��ָ���������ͣ��Ա���Ҷ�ڵ����ܹ����ú��ʵ�ģ��
			����Ҷ�ڵ����ݽ���Ԥ��ĺ���������
	returns:
		
	'''
	if not isTree(tree):
		#�����Ҷ�ڵ㣬��ֱ�ӽ���Ԥ��
		return modelEval(tree,inData)
		
	#���������ݵ�ָ������ֵ>tree�ڵ��������ֵ  
	#��ʱ����������
	if inData[tree['spInd']]>tree['spVal']:
		if isTree(tree['left']):
			return treeForeCast(tree['left'],inData,modelEval)
		else:
			return modelEval(tree['left'],inData)
	#���������ݵ�ָ������ֵ<=tree�ڵ��������ֵ  
	#��ʱ����������
	else:
		if isTree(tree['right']):
			return treeForeCast(tree['right'],inData,modelEval)
		else:
			return modelEval(tree['right'],inData)


def createForeCast(tree,testData,modelEval=regTreeEval):
	'''��ε���treeForcast���� 
	parameters:
		tree:ѵ�����������ṹ
		testData:��������
		modelEval:������
	returns:
		yHat:�������ݵ�Ԥ����
	'''
	m=len(testData)
	yHat=mat(zeros((m,1)))
	for i in range(m):
		yHat[i,0]=treeForeCast(tree,mat(testData[i]),modelEval)
	return yHat
			

 
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	












