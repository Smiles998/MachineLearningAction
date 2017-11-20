#coding=gbk
from time import sleep
import json
import urllib.request

#示例：用回归法预测乐高套装的价格
'''
步骤如下：
	。收集收据：用Google shopping的API收集数据
	。准备数据：从返回的JSON数据中抽取价格
	。分析数据：可视化并观察数据
	。训练算法：构建不同的模型，采用逐步线性回归和直接的线性回归模型
	。测试算法：使用交叉验证来测试不同的模型，分析哪个效果最好
	。使用算法：此次练习的目标就是生成数据模型
'''

#收集数据：使用Google购物的API
#购物信息的获取函数
def searchForSet(retX,retY,setNum,yr,numPce,origPrc):
	''' 调用Google购物API并保证数据抽取的正确性
	
	
	'''
	#推迟调用线程的运行，表示进程挂起的时间
	sleep(10)#休眠10秒，防止短时间内有过多的API调用
	myAPIstr='get from code.google.com'
	searchURL='https://www.googleapis.com/shopping/search/v1/public/\
				products?key=%s&country=US&q=lego+%d&alt=json' %(myAPIstr,setNum)
	#调用API
	pg= urllib.request.urlopen(searchURL)
	#抽取数据--->打开和解析操作
	retDict=json.loads(pg.read())
	
	for i in range( len(retDict['items']) ):
		try:
			currItem=retDict['items'][i]
			if currItem['product']['condition']=='new':
				newFlag=1
			else:
				newFlag=0
			listOfInv=currItem['product']['inventories']
			for item in listOfInv:
				sellingPrice=item['price']
				#确定套装是否完整
				if sellingPrice>origPrc*0.5:
					print("%d\t%d\t%d\t%f\t%f" %(yr,numPce,newFlag,origPrc,sellingPrice))
					#套装的一些信息--->用此些信息来估计套装的价格
					retX.append([yr,numPce,newFlag,origPrc])
					#套装的价格
					retY.append(sellingPrice)  				
		except:
			print("problem with item %d" %i)
					
def setDataCollection(retX,retY):
	searchForSet(retX,retY,8288,2006,800,49.99)
	searchForSet(retX,retY,10030,2002,3096,269.99)
	searchForSet(retX,retY,10179,2007,5195,499.99)
	searchForSet(retX,retY,10181,2007,3428,199.99)
	searchForSet(retX,retY,10189,2008,5922,299.99)
	searchForSet(retX,retY,10196,2009,3262,249.99)
	
#以上两个函数为收集数据，但是运行的时候，被连接主机并无反应
			

#下面使用交叉验证测试岭回归			









	
