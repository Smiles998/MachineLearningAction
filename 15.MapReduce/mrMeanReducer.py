# coding=gbk
'''分布式均值和方差计算的reducer '''
import sys
from numpy import *

#接受Mapper的输出，并将它们合并称为全局的均值和方差

def read_input(fileName):
	for line in fileName:
		yield line.rstrip()
		
inputRed=read_input(sys.stdin)
mapperOut=[line.split('\t') for line in inputRed  ]

cumVal=0.0
cumSumSq=0.0
cumN=0.0

for instance in mapperOut:
	nj=float(instance[0]) 
	cumN+=nj
	cumVal+=nj*float(instance[1])
	cumSumSq+=nj*float(instance[2])
	
mean=cumVal/cumN
varSum=(cumSumSq-2*mean*cumVal+cumN*mean*mean)/cumN
print("%d\t%f\t%f" %(cumN,mean,varSum))

print("report:still alive",file=sys.stderr)


















































