#coding=gbk
from tkinter import*

''' 
	Python���кܶ�GUI��ܣ�����һ������ʹ�õ�Tkiner������Python�ı�׼����汾������
  Tkinter��GUI��һЩС������ɣ���νС������ָ�����ı���(Text Box),��ť(Button),
��ǩ(Label)�͸�ѡ��ť(Check Button)�ȶ���
	
'''
#����һ������
root=Tk()
#�ڴ�������ʾһЩ����
myLabel=Label(root,text="Hello World")
#������grid()����ʱ���͵��ڰ�myLabel��λ�ø����˲��ֹ�������Tkinter���ṩ�˼��ֲ�ͬ�Ĳ��ֹ�������
#����.grid()�������С����������һ����ά�ı���У��û������趨ÿ��С�������ڵ�����λ�ã�Ĭ����ʾ��0��0��

myLabel.grid()
#����ʱ��ѭ����ʹ�ô������ڶ��¼��п�����Ӧ��������������ػ�ȶ���
root.mainloop()
