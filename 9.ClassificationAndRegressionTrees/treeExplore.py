#coding=gbk
#���潫Tkinter�е�GUI�е�С����������һ�𹹽���������
from numpy import*
from tkinter import*
import matplotlib
matplotlib.use('TkAgg')#�趨���ΪTkAgg
#��TkAgg��Matplotlibͼ��������
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import regTrees

'''
Tkinter��GUI��һЩС������ɣ���νС������ָ����
	�ı���(Text Box)
	��ť(Button),
	��ǩ(Label),
	��ѡ��ť(Check Button)
	�ı������(Entry):һ���������ı�������ı���
	��ť����ֵ(IntVar)
	�ȶ���
'''
#���ڹ�������������TkinterС����
#��������ռλ������
def reDraw(tolS,tolN):
	#���֮ǰ��ͼ��ʹ��ǰ������ͼ�񲻻��ص�
	reDraw.f.clf()
	reDraw.a=reDraw.f.add_subplot(111)
	if chkBtnVar.get():#��鸴ѡ���Ƿ�ѡ�У���Ϊ��ģ��
		if tolN<2:
			tolN=2
		myTree=regTrees.createTree(reDraw.rawDat,regTrees.modelLeaf,regTrees.modelErr,(tolS,tolN))
		yHat=regTrees.createForeCast(myTree,reDraw.testDat,regTrees.modelTreeEval)
	else:#����Ϊ�ع�ģ��
		myTree=regTrees.createTree(reDraw.rawDat,ops=(tolS,tolN))
		yHat=regTrees.createForeCast(myTree,reDraw.testDat)
		
	reDraw.a.scatter(list(reDraw.rawDat[:,0]),list(reDraw.rawDat[:,1]),s=5)
	reDraw.a.plot(reDraw.testDat,yHat,linewidth=2.0)
	reDraw.canvas.show()
	
	
def getInputs():
	try:
		tolN=int(tolNentry.get())
	except:
		tolN=10#����ΪĬ�ϵ�ֵ
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
	tolN,tolS=getInputs()#�õ�������ֵ
	reDraw(tolS,tolN)
	
#����һ��GUI����
#1.���ȴ���һ��Tk���͵ĸ�����
root=Tk()
#2.Ȼ������ǩ������ʹ��.grid()�����趨�к��е�λ�ã�Ҳ����ͨ��columnspan��rowspan�����߲��ֹ������Ƿ�����һ��С��������/����
#Label(root,text="Plot Place Holder").grid(row=0,columnspan=3)

#��matplotlib�Ļ�ͼǶ�뵽Tkinter��GUI������
reDraw.f=plt.figure(figsize=(5,4),dpi=100)
reDraw.canvas=FigureCanvasTkAgg(reDraw.f,master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0,columnspan=3)#����ͼ��λ��



Label(root,text="tolN").grid(row=1,column=0)
#Entry������һ���������ı�������ı���
tolNentry=Entry(root)
tolNentry.grid(row=1,column=1)
tolNentry.insert(0,'10')

Label(root,text="tolS").grid(row=2,column=0)
tolSentry=Entry(root)
tolSentry.grid(row=2,column=1)
tolSentry.insert(0,'1.0')

#����ͼ�ΰ�ť�������˵��ReDraw��ťʱ������Ҫ����command����
Button(root,text="ReDraw",command=drawNewTree).grid(row=1,column=2)
#�˳���ť
Button(root,text='Quit',fg='black',command=root.quit).grid(row=2,column=2)

chkBtnVar=IntVar()
chkBtn=Checkbutton(root,text="Model Tree",variable=chkBtnVar)
chkBtn.grid(row=3,column=0,columnspan=2)

#��ʼ��һЩ��reDraw()������ȫ�ֱ���
reDraw.rawDat=mat(regTrees.loadDataSet('sine.txt'))
reDraw.testDat=arange( min(reDraw.rawDat[:,0]),max(reDraw.rawDat[:,0]),0.01)
reDraw(1.0,10)







root.mainloop()


































