
#FP树节点的类定义
class treeNode:
	def __init__(self,nameValue,numOccur,parentNode):
		self.name=nameValue     #节点的名字
		self.count=numOccur  	#频数计数器
		self.nodeLink=None		#相似节点的链接
		self.parent=parentNode  #父节点
		self.children={}		    #子节点

	def inc(self,numOccur):
		#对count变量增加给定值
		self.count+=numOccur 
		
	def disp(self,ind=1):#默认从根节点开始显示
		#将树以文本形式进行显示
		print("%d,%s\t%d" %(ind,self.name,self.count))
		for child in self.children.values():
			child.disp(ind+1)



#FP树构建函数
def createTree(dataSet,minSup=1):
	'''构建FP树
	parameters:
		dataSet:事务数据集
		minSup:最小支持度
	returns:
		retTree：FP-tree的root节点
		headerTable：头指针表
	'''
	#得到头指针表
	#print("#得到头指针表")
	headerTable={}
	for trans in dataSet:#对事务数据库中的每个事务
		for item in trans:#对事务项集中每个项
			headerTable[item]=headerTable.get(item,0)+dataSet[trans]#？？
	#print("#移除不满足最小支持度的元素项")	
	#移除不满足最小支持度的元素项
	for k in list(headerTable.keys()):
		if headerTable[k]<minSup:
			del headerTable[k]
	
	#剩余的为所有的频繁项集
	freqItemSet=set(headerTable.keys())
	if len(freqItemSet)==0:
		return None,None
	
#	print("#重新安排头指针表，需要包含一个指针，指向树中的相似元素	")
	#重新安排头指针表，需要包含一个指针，指向树中的相似元素	
	for k in headerTable:
		headerTable[k]=[headerTable[k],None]
	#print("#创建树的根节点")
	#创建树的根节点
	retTree=treeNode('Null Set',1,None)
	
	#dataSet是一个字典{事务：事务出现的次数}-->相当于事务存在着重复
	for transSet,count in dataSet.items():
		localD={}
	#	print("取得事务中的频繁项以及其支持度")
		for item in transSet:
			if item in freqItemSet: #取得事务中的频繁项以及其支持度
				localD[item]=headerTable[item][0]
	#	print("#按照其支持度进行排序#将该频繁项集插入到FP-tree中")
		#对其进行排序		
		if len(localD)>0:
			#按照其支持度进行排序
			orderedItems=[v[0] for v in sorted(localD.items(),\
							key=lambda p:p[1],reverse=True)]
			#将该频繁项集插入到FP-tree中
			updateTree(orderedItems,retTree,headerTable,count)
			
	return retTree,headerTable
	
	
	
def updateTree(items,inTree,headerTable,count):
	'''将频繁项集items加入到FP-tree中
	parametes:
		items:事务中的频繁项集
		inTree:需要构建的树的根节点(递归调用使用方式)
		headerTable:头指针表
		count:
	returns:
		
	'''
	if items[0] in inTree.children:#当前元素是否存在于字典中
	#	print("当前子节点存在，则此时需要增加其计数")
		inTree.children[items[0]].inc(count)
	else:#当前元素不存在，则需要向树添加一个分支(添加一个节点)
	#	print("构建root节点的子节点")--->此处会建立起指向父节点的关系
		inTree.children[items[0]]=treeNode(items[0],count,inTree)
	
	##更新头指针表
#	print("更新头指针表")
	if headerTable[items[0]][1]==None:
		headerTable[items[0]][1]=inTree.children[items[0]]
	else:
		updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
	
	#递归更新FP-tree	
	if len(items)>1:
		#print("递归构建FP-tree	")
		#items[1::] 列表切分，从第二个元素到最后一个元素
		updateTree(items[1::],inTree.children[items[0]],headerTable,count)
	
	
def updateHeader(nodeToTest,targetNode):
	print("连接相似节点")
	#???此处是一个无限循环，没有合适的退出条件
	if nodeToTest==targetNode:
		print("此时插入节点与头指针表中相同")
		return
	while (nodeToTest.nodeLink!=None):	
		if nodeToTest==targetNode:
			print("此时插入节点与已在链表中")
			return
		nodeToTest=nodeToTest.nodeLink	
	#在此处一直有一个疑问？？？当链表最后一个节点和所插入节点一模一样时此时并不需要将其进行插入
	print("为链表添加一个相似项")
	nodeToTest.nodeLink=targetNode

			
def loadSimpData():
	simpData=[  ['r','z','h','j','p'],
				['z','y','x','w','v','u','t','s'],
				['z'],
				['r','x','n','o','s'],
				['y','r','x','z','q','t','p'],
				['y','z','x','e','q','s','q','s','t','m']]
	return simpData
	
def createInitSet(dataSet):
	retDict={}
	for trans in dataSet:
		retDict[frozenset(trans)]=1
	return retDict



'''以下两个函数用于为给定元素项生成一个条件模式基
条件模式基：前缀路径以及其计数
'''
#发现以给定元素项结尾的所有路径的函数（前缀路径发现）
def ascendTree(leafNode,prefixPath):
	'''前缀路径发现 --->介于查找元素项与树根节点之间的所有内容
	parameters:
		leafNode:从该节点找其前缀路径
		prefixPath:前缀路径的存放位置
	'''
	if leafNode.parent!=None:
		prefixPath.append(leafNode.name)
		ascendTree(leafNode.parent,prefixPath)#迭代上溯整棵树
		
def findPrefixPath(basePat,treeNode):
	'''前缀路径发现 ---
	parameters:
		basePat:
		treeNode:
	returns:
		condPat:发现的所有元素项的条件模式基-->前缀路径
			是一个字典结构：{前缀路径：出现次数}
	'''
	#条件模式字典--->也就是所有的前缀路径
	condPats={}
	#遍历链表直至到达结尾,每遇到的一个元素项都会调用ascendTree()来上溯FP树，并收集所遇到的元素项的名称
	while treeNode!=None:
		prefixPath=[]
		ascendTree(treeNode,prefixPath)
		if len(prefixPath)>1:
			condPats[frozenset(prefixPath[1:])]=treeNode.count
			
		treeNode=treeNode.nodeLink
	
	return condPats


#以下为创建条件FP树
'''对于每一个频繁项，都要创建一棵条件FP树 '''
#递归查找频繁项集的minTree函数
def minTree(inTree,headerTable,minSup,preFix,freqItemList):
	''' 
	parameters:
		inTree:FP-growth tree
		headerTable:头指针
		minSup:最小支持度阈值
		preFix:  前缀路径（初始时为空）
		freqItemList:频繁项集（初始时为空）
	returns:
		
	'''
	#对头指针表中的元素项按照其出现的频率进行排序(默认顺序：从小到大)-->得到的是按支持度排序的元素列表
	print("------------------")
	print(headerTable.items())
	bigL=[v[0] for v in sorted(headerTable.items(),key=lambda p:p[1][0])  ]
	
	for basePat in bigL:#对于每一个频繁项
		newFreqSet=preFix.copy() #新的频繁项集
		newFreqSet.add(basePat)
		freqItemList.append(newFreqSet)
		#找到频繁项basePat的所有条件基
		condPattBases=findPrefixPath(basePat,headerTable[basePat][1])
		#该条件基被当作一个新数据集输送给createTree()函数
		myCondTree,myHead=createTree(condPattBases,minSup)
		print("conditional tree for: "+str(newFreqSet))
		if myCondTree!=None:
			myCondTree.disp()
		
		if myHead!=None:
			#还可以再接着构建
			minTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)


























