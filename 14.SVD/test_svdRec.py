# coding=gbk
from numpy import*
from numpy import linalg as la

import svdRec

'''
#测试SVD分解
Data=svdRec.loadExData()
U,Sigma,VT=linalg.svd(Data)

print("Sigma:")
print(Sigma)

#对原始矩阵进行重构
Sig3=mat([ [Sigma[0],0,0],[0,Sigma[1],0],[0,0,Sigma[2]] ])
print("重构之后的原始矩阵为：")
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


#推荐排序
#利用基于物品相似度和多个相似度计算方法来进行推荐

myMat=mat(svdRec.loadExData())

myMat[0,1]=myMat[0,0]=myMat[1,0]=myMat[2,0]=4
myMat[3,3]=2

print("myMat:")
print(myMat)

rec=svdRec.recommend(myMat,2)
print("用User2所推荐的产品：")
print(rec)

rec1=svdRec.recommend(myMat,2,simMeas=svdRec.ecludSim)
print("用User2所推荐的产品：")
print(rec1)

rec2=svdRec.recommend(myMat,2,simMeas=svdRec.pearsSim)
print("用User2所推荐的产品：")
print(rec2)


#使用SVD提高推荐的效果
U,Sigma,VT=la.svd(mat(svdRec.loadExData2()))
print(Sigma)


Sigma2=Sigma**2
sumSigma2=sum(Sigma2)
sumSigma2*0.9





myMat = mat(svdRec.loadExData2())

rec=svdRec.recommend(myMat,1,estMethod=svdRec.svdEst)
print("用User1所推荐的产品：")
print(rec)

rec1=svdRec.recommend(myMat,1,estMethod=svdRec.svdEst,simMeas=svdRec.ecludSim)
print("用User1所推荐的产品：")
print(rec1)

rec2=svdRec.recommend(myMat,1,estMethod=svdRec.svdEst,simMeas=svdRec.pearsSim)
print("用User1所推荐的产品：")
print(rec2)


'''

svdRec.imgCompress()




















