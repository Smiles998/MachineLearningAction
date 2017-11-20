#coding=gbk
#下面将Tkinter中的GUI中的小部件集成在一起构建树管理器
from numpy import*
from tkinter import*
import matplotlib
matplotlib.use('TkAgg')#设定后端为TkAgg
#将TkAgg和Matplotlib图链接起来
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import regTrees

'''
Tkinter的GUI由一些小部件组成，所谓小部件，指的是
	文本框(Text Box)
	按钮(Button),
	标签(Label),
	复选按钮(Check Button)
	文本输入框(Entry):一个允许单行文本输入的文本框
	按钮整数值(IntVar)
	等对象
'''
#用于构建树管理界面的Tkinter小部件
#两个绘制占位符函数
def reDraw(tolS,tolN):
	#清空之前的图像，使得前后两个图像不会重叠
	reDraw.f.clf()
	reDraw.a=reDraw.f.add_subplot(111)
	if chkBtnVar.get():#检查复选框是否选中，则为树模型
		if tolN<2:
			tolN=2
		myTree=regTrees.createTree(reDraw.rawDat,regTrees.modelLeaf,regTrees.modelErr,(tolS,tolN))
		yHat=regTrees.createForeCast(myTree,reDraw.testDat,regTrees.modelTreeEval)
	else:#否则为回归模型
		myTree=regTrees.createTree(reDraw.rawDat,ops=(tolS,tolN))
		yHat=regTrees.createForeCast(myTree,reDraw.testDat)
		
	reDraw.a.scatter(list(reDraw.rawDat[:,0]),list(reDraw.rawDat[:,1]),s=5)
	reDraw.a.plot(reDraw.testDat,yHat,linewidth=2.0)
	reDraw.canvas.show()
	
	
def getInputs():
	try:
		tolN=int(tolNentry.get())
	except:
		tolN=10#设置为默认的值
		print("enter Integer for tolN")
		tolNentry.delete(0,END)
		tolNentry.insert(0,'10')
	try:
		tolS=float(tolSentry.get())
	except:
		tolS=1.0
		print("enter Float for tolS")
		tolSentry.delete(0,END)
		tolSentry.insert(0,'1.0')
	return tolN,tolS
	
def drawNewTree():
	tolN,tolS=getInputs()#得到输入框的值
	reDraw(tolS,tolN)
	
#创建一个GUI窗口
#1.首先创建一个Tk类型的根部件
root=Tk()
#2.然后插入标签，并且使用.grid()方法设定行和列的位置，也可以通过columnspan和rowspan来告诉布局管理器是否允许一个小部件跨列/跨行
#Label(root,text="Plot Place Holder").grid(row=0,columnspan=3)

#将matplotlib的绘图嵌入到Tkinter的GUI界面中
reDraw.f=plt.figure(figsize=(5,4),dpi=100)
reDraw.canvas=FigureCanvasTkAgg(reDraw.f,master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0,columnspan=3)#绘制图的位置



Label(root,text="tolN").grid(row=1,column=0)
#Entry部件是一个允许单行文本输入的文本框
tolNentry=Entry(root)
tolNentry.grid(row=1,column=1)
tolNentry.insert(0,'10')

Label(root,text="tolS").grid(row=2,column=0)
tolSentry=Entry(root)
tolSentry.grid(row=2,column=1)
tolSentry.insert(0,'1.0')

#绘制图形按钮，在有人点击ReDraw按钮时，就需要调用command命令
Button(root,text="ReDraw",command=drawNewTree).grid(row=1,column=2)
#退出按钮
Button(root,text='Quit',fg='black',command=root.quit).grid(row=2,column=2)

chkBtnVar=IntVar()
chkBtn=Checkbutton(root,text="Model Tree",variable=chkBtnVar)
chkBtn.grid(row=3,column=0,columnspan=2)

#初始化一些与reDraw()关联的全局变量
reDraw.rawDat=mat(regTrees.loadDataSet('sine.txt'))
reDraw.testDat=arange( min(reDraw.rawDat[:,0]),max(reDraw.rawDat[:,0]),0.01)
reDraw(1.0,10)







root.mainloop()


































