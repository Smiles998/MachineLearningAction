import trees
import treePlotter

filename = 'lenses.txt'
with open(filename) as f:
	lensensLists =  [ line.strip().split('\t')  for line in  f.readlines()]

lensensLabels = ['age','prescript','astigmatic','tearRate']

lensensTree = trees.createTree(lensensLists,lensensLabels)

print(lensensTree)
treePlotter.createPlot(lensensTree)
