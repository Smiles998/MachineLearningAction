import matplotlib.pyplot as plt
#动态设置参数解决matplotlib的中文问题显示问题
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']#指定默认字体
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像时，负号‘-’显示为方块的问题

#定义决策树决策结果的属性，用字典来定义
#1.树节点格式常量
'''下面的字典定义也可写作，decisionNode = { boxstyle:'sawtooth',fc:'0.8' }
boxstyle为文本框的类型，sawtooth是锯齿形，fc是边框线粗细
'''
decisionNode = dict( boxstyle = 'sawtooth', fc='0.8' )
#定义决策树的叶子节点的描述属性
leafNode = dict( boxstyle='round4', fc='0.8')
#定义决策树的箭头属性
arrow_args = dict(arrowstyle='<-')

#绘制结点--->实际的绘图功能
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
	#annotate是一个关于数据点的文本
	#nodeTxt为要显示的文本，centerPt为文本的中心点，parentPt为箭头开始的点，箭头指向为（parentPt->centerPt）
	#在句柄上添加结点--->即在绘图区域中添加结点
	createPlot.ax1.annotate( nodeTxt,					#该注解要显示的文本
			xy=parentPt,xycoords = 'axes fraction', 	#箭头的起始点
			xytext=centerPt,textcoords='axes fraction', #箭头的结束点，即文本显示所在的点
			va='center',ha='center',					#设置水平和垂直居中
			bbox=nodeType,arrowprops=arrow_args)		#文本框显示类型和箭头类型

#创建绘图
'''
此为第一个版本
def createPlot():
	#类似于Matlab的figure,定义一个figure，背景为白色
	#--->figure是一个top level container 包含了所有的plot elements
	fig = plt.figure(1,facecolor='yellow')
	fig.clf()#把figure清空
	#plt.subplot()-->返回一个figure subplot的句柄 frameon=False-->此属性可以去掉坐标轴
	createPlot.ax1=plt.subplot(111,frameon=False)#将figure区域进行划分
	plotNode('决策节点',(0.8,0.1),(0.5,0.5),decisionNode)
	plotNode('叶节点',(0.1,0.1),(0.8,0.8),leafNode)
	plt.show()
	
'''

#只需要知道决策树的字典结构就可以很容易地求出叶子个数和树高
def getNumLeafs(myTree):
	''' 得到所有的叶子数，从而可以有效地确定x轴的长度'''
	numLeafs = 0
	firstStr =list(myTree.keys())[0]    #得到最顶层的决策节点--->root
	secondDict = myTree[firstStr]		#划分的数据集节点
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ != 'dict':
			numLeafs += 1
		else:
			numLeafs += getNumLeafs(secondDict[key])
			
	return numLeafs
	
def getTreeDepth(myTree):
	''' 得到树的深度，从而可以有效地确定y轴的高度'''
	maxDepth = 0
	firstStr = list(myTree.keys())[0]		#得到最顶层的决策节点---->root
	secondDict = myTree[firstStr] 		    #划分的数据集
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			thisDepth = 1+getTreeDepth(secondDict[key])
		else:
			thisDepth = 1+1
		if thisDepth > maxDepth: maxDepth = thisDepth
	
	return maxDepth	
		
#以下函数为预先存储的树信息，避免了每次测试代码时都要从数据中创建数的麻烦
def retrieveTree(i):
	listOfTrees = [{ "no surfacing":{ 0:'no',
				    	1:{'flippers': {0:'no', 1:'yes'}}}},
					{'no surfacing':{0:'no',1:{'flippers':
						{0: {'header':{0:'no',1:'yes'}},1:'no'}}}}
				  ]
				  
	return listOfTrees[i]
	
'''	
print(retrieveTree(0)	)
print(getNumLeafs(retrieveTree(0)))
print(getTreeDepth(retrieveTree(0)))
'''

def plotMidText(cntrPt,parentPt,txtString):
	''' 在父子节点间填充文本信息-->划分数据集时的特征的取值情况
	parameters:
		cntPt:the the position of children node ->(x,y)
		parentPt: the position of parent node ->(x,y)
		txtString：the text string showed between parents and children
	'''
	xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
	yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
	
	createPlot.ax1.text(xMid,yMid,txtString) 
	
def plotTree(myTree,parentPt,nodeTxt):
	'''绘制决策树
	parameters:
		myTree:要绘制的树的字典结构
		parentPt:父节点所在的位置坐标
		nodeText:节点文本
	'''
	numLeafs = getNumLeafs(myTree)  #计算宽
	depth = getTreeDepth(myTree)    #计算高
	#得到当前树根节点的特征属性
	firstStr = list(myTree.keys())[0]
	#坐标轴的默认范围为：[0.0---1.0]
	#plotTree也是一个全局变量，在程序中都可以使用 ???为什么要如此计算还是有些不太清楚和明白    
	cntrPt = (plotTree.xOff +(1.0+ float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
	#得到其中间节点
	plotMidText(cntrPt,parentPt,nodeTxt)#其实此步骤并不是很清楚
	plotNode(firstStr,cntrPt,parentPt,decisionNode)#绘制当前决策节点
	
	secondDict = myTree[firstStr]		#得到其数据集划分，根据特征firstStr的值进行数据集划分
	plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD #坐标向树的下一层移动
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':#对树进行递归绘制
			plotTree(secondDict[key],cntrPt,str(key))
		else:
			#此时需要绘制一个叶子节点
			#计算叶子节点的横坐标
			plotTree.xOff = plotTree.xOff +1.0/plotTree.totalW
			plotNode(secondDict[key], (plotTree.xOff,plotTree.yOff),cntrPt,leafNode )
			plotMidText( (plotTree.xOff, plotTree.yOff),cntrPt,str(key) )
	#在绘制了所有子节点之后，增加全局变量Y的偏移--->回到上一个判断节点
	plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
	
#改进后的createPlot版本
def createPlot(inTree):
	#创建一个figure对象，作为绘制面板,并清空其所有内容
	fig = plt.figure(1,facecolor='green')
	fig.clf()
	#定义横纵坐标轴，无内容--->控制没有坐标轴标度
	axprops = dict(xticks=[],yticks=[])
	#绘制图像，无边框，无坐标轴    **axprops-->变参字典形式
	#createPlot.ax1=plt.subplot(111,frameon=False,**axprops)#使用函数属性实现全局变量
	createPlot.ax1=plt.subplot(111)
	#保存树宽
	plotTree.totalW = float(getNumLeafs(inTree)) 
	#保存树高
	plotTree.totalD = float(getTreeDepth(inTree)) 
	#决策树起始横坐标
	plotTree.xOff = -0.5/plotTree.totalW#从零开始会偏右
	print("plotTree.xOff=" + str(plotTree.xOff))
	#决策树的起始纵坐标
	plotTree.yOff = 1.0
	#绘制决策树-->inTree:root节点， 
	plotTree(inTree,(0.5, 1.0),'')
	#显示图像
	plt.show()
	































