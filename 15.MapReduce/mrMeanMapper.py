'''分布式均值和方差计算的mapper'''
import sys
from numpy import*

def read_input(fileName):
	for line in fileName:
		yield line.rstrip()
		
#从标准输入设备中按行读取所有的输入并创建一组对应的浮点数	
inputData = read_input(sys.stdin)
inputData=[float(line) for line in inputData  ]

#得到该数组的长度
numInputs=len(inputData)
inputData=mat(inputData)
sqInputData=power(inputData,2)#逐个元素做运算

#标准输出，也就是reduce的输入
print("%d\t%f\t%f" %(numInputs,mean(inputData),mean(sqInputData)))

#标准错误输出：即对主节点作出的响应报告，标明本节点工作正常
print("report: still alive",file=sys.stderr)


