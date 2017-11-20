#coding=gbk
from time import sleep
import json
import urllib.request

#ʾ�����ûع鷨Ԥ���ָ���װ�ļ۸�
'''
�������£�
	���ռ��վݣ���Google shopping��API�ռ�����
	��׼�����ݣ��ӷ��ص�JSON�����г�ȡ�۸�
	���������ݣ����ӻ����۲�����
	��ѵ���㷨��������ͬ��ģ�ͣ����������Իع��ֱ�ӵ����Իع�ģ��
	�������㷨��ʹ�ý�����֤�����Բ�ͬ��ģ�ͣ������ĸ�Ч�����
	��ʹ���㷨���˴���ϰ��Ŀ�������������ģ��
'''

#�ռ����ݣ�ʹ��Google�����API
#������Ϣ�Ļ�ȡ����
def searchForSet(retX,retY,setNum,yr,numPce,origPrc):
	''' ����Google����API����֤���ݳ�ȡ����ȷ��
	
	
	'''
	#�Ƴٵ����̵߳����У���ʾ���̹����ʱ��
	sleep(10)#����10�룬��ֹ��ʱ�����й����API����
	myAPIstr='get from code.google.com'
	searchURL='https://www.googleapis.com/shopping/search/v1/public/\
				products?key=%s&country=US&q=lego+%d&alt=json' %(myAPIstr,setNum)
	#����API
	pg= urllib.request.urlopen(searchURL)
	#��ȡ����--->�򿪺ͽ�������
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
				#ȷ����װ�Ƿ�����
				if sellingPrice>origPrc*0.5:
					print("%d\t%d\t%d\t%f\t%f" %(yr,numPce,newFlag,origPrc,sellingPrice))
					#��װ��һЩ��Ϣ--->�ô�Щ��Ϣ��������װ�ļ۸�
					retX.append([yr,numPce,newFlag,origPrc])
					#��װ�ļ۸�
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
	
#������������Ϊ�ռ����ݣ��������е�ʱ�򣬱������������޷�Ӧ
			

#����ʹ�ý�����֤������ع�			









	
