from utility import *

from alg import getDecomposition

def updateDecomposition(edgeDataList, layerDict, waveDict, fragDict):
	for edge in edgeDataList:
		s, t = edge['source'], edge['target']
		edge['layer'] = layerDict[(s, t)]
		edge['wave'] = waveDict[(s, t)]
		edge['fragment'] = fragDict[(s, t)]
	return edgeDataList

if __name__ == '__main__':
	## read data
	name = 'asoiaf'
	# name = 'njals_saga'

	fileColIntList = ['source', 'target', 'weight']
	dataKeyIntList = ['source', 'target', 'value']
	# fileColIntList = ['source', 'target', 'value', 'direction', 'cycle']
	# dataKeyIntList = fileColIntList

	edgeDataList = readCSV(f'dataset/{name}_edges-numbered.csv', fileColIntList, dataKeyIntList)
	# edgeDataList = readCSV(f'dataset/{name}_edges_multi.csv', fileColIntList, dataKeyIntList)


	## prepare input
	edgeList = [(edge['source'], edge['target']) for edge in edgeDataList if edge['source'] != edge['target']]


	## compute fixpoint and wave\fragment decomposition
	## [(x, y)] -> {(x, y): fixpoint}, {(x, y): wave}, {(x, y): fragment}
	layerDict, waveDict, fragDict = getDecomposition(edgeList)

	## update edge data
	edgeDataList = updateDecomposition(edgeDataList, layerDict, waveDict, fragDict)

	## write data
	fileColList = ['source', 'target', 'value', 'layer', 'wave', 'fragment']
	# fileColList = ['source', 'target', 'value', 'direction', 'cycle', 'layer', 'wave', 'fragment']
	writeCSVDict(f'dataset/preprocess/{name}_edges_decomposition.csv', fileColList, edgeDataList)