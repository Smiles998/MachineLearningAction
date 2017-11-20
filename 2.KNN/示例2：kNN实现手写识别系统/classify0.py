def classify0(inX,dataSet,labels,k):
    '''
indx:用于分类的输入向量
dataSet:train dataset
label:  the labels for train dataset
k:用于选择最近邻的数目
    '''
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistances=sqDistances**0.5
    sortedDistIndicies=distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlable]=classCount.get(voteIlable,0)+1
        sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
        return sortedClassCount[0][0]
