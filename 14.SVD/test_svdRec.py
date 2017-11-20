# coding=gbk
from numpy import*
from numpy import linalg as la

import svdRec

'''
#����SVD�ֽ�
Data=svdRec.loadExData()
U,Sigma,VT=linalg.svd(Data)

print("Sigma:")
print(Sigma)

#��ԭʼ��������ع�
Sig3=mat([ [Sigma[0],0,0],[0,Sigma[1],0],[0,0,Sigma[2]] ])
print("�ع�֮���ԭʼ����Ϊ��")
print(U[:,:3]*Sig3*VT[:3,:])


myMat=mat(svdRec.loadExData())

print("ecludSim:")
print(svdRec.ecludSim(myMat[:,0],myMat[:,4]))

print("ecludSim:")
print(svdRec.ecludSim(myMat[:,0],myMat[:,0]))

print("cosdSim:")
print(svdRec.cosSim(myMat[:,0],myMat[:,4]))

print("cosSim:")
print(svdRec.cosSim(myMat[:,0],myMat[:,0]))


print("pearsSim:")
print(svdRec.pearsSim(myMat[:,0],myMat[:,4]))

print("pearsSim:")
print(svdRec.pearsSim(myMat[:,0],myMat[:,0]))


#�Ƽ�����
#���û�����Ʒ���ƶȺͶ�����ƶȼ��㷽���������Ƽ�

myMat=mat(svdRec.loadExData())

myMat[0,1]=myMat[0,0]=myMat[1,0]=myMat[2,0]=4
myMat[3,3]=2

print("myMat:")
print(myMat)

rec=svdRec.recommend(myMat,2)
print("��User2���Ƽ��Ĳ�Ʒ��")
print(rec)

rec1=svdRec.recommend(myMat,2,simMeas=svdRec.ecludSim)
print("��User2���Ƽ��Ĳ�Ʒ��")
print(rec1)

rec2=svdRec.recommend(myMat,2,simMeas=svdRec.pearsSim)
print("��User2���Ƽ��Ĳ�Ʒ��")
print(rec2)


#ʹ��SVD����Ƽ���Ч��
U,Sigma,VT=la.svd(mat(svdRec.loadExData2()))
print(Sigma)


Sigma2=Sigma**2
sumSigma2=sum(Sigma2)
sumSigma2*0.9





myMat = mat(svdRec.loadExData2())

rec=svdRec.recommend(myMat,1,estMethod=svdRec.svdEst)
print("��User1���Ƽ��Ĳ�Ʒ��")
print(rec)

rec1=svdRec.recommend(myMat,1,estMethod=svdRec.svdEst,simMeas=svdRec.ecludSim)
print("��User1���Ƽ��Ĳ�Ʒ��")
print(rec1)

rec2=svdRec.recommend(myMat,1,estMethod=svdRec.svdEst,simMeas=svdRec.pearsSim)
print("��User1���Ƽ��Ĳ�Ʒ��")
print(rec2)


'''

svdRec.imgCompress()




















