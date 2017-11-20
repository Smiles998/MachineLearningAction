# coding=gbk
import treePlotter

'''
#测试绘制图形--->第一个版本
#treePlotter.createPlot()

#测试得到树高和叶子数
print(treePlotter.retrieveTree(0)	)
print(treePlotter.getNumLeafs(treePlotter.retrieveTree(0)))
print(treePlotter.getTreeDepth(treePlotter.retrieveTree(0)))
'''

myTree = treePlotter.retrieveTree(1)
treePlotter.createPlot(myTree)
