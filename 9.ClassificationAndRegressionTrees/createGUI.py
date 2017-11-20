#coding=gbk
from tkinter import*

''' 
	Python中有很多GUI框架，其中一个易于使用的Tkiner是随着Python的标准编译版本发布的
  Tkinter的GUI由一些小部件组成，所谓小部件，指的是文本框(Text Box),按钮(Button),
标签(Label)和复选按钮(Check Button)等对象
	
'''
#创建一个窗口
root=Tk()
#在窗口上显示一些文字
myLabel=Label(root,text="Hello World")
#当调用grid()方法时，就等于把myLabel的位置告诉了布局管理器。Tkinter中提供了几种不同的布局管理器，
#其中.grid()方法会把小部件安排在一个二维的表格中，用户可以设定每个小部件所在的行列位置，默认显示在0行0列

myLabel.grid()
#启动时间循环，使该窗口在众多事件中可以响应鼠标点击、按键和重绘等动作
root.mainloop()
