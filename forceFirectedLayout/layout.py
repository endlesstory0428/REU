import numpy as np
import json

from utility import *
from template import getHTML

def getColorGroup(dataList, key, bucketFlag = True):
	if key is None:
		for data in dataList:
			data['colorGroup'] = 0
		return dataList, 1
		
	weightList = np.array([data[key] for data in dataList], dtype = np.float64)

	if not bucketFlag:
		for idx, data in enumerate(dataList):
			data['colorGroup'] = int(weightList[idx])
		return dataList, int(np.max(weightList))

	aveWeight = np.mean(weightList)
	stdWeight = np.std(weightList)
	negBinNum = np.ceil((aveWeight - np.min(weightList)) / stdWeight)
	posBinNum = np.ceil((np.max(weightList) - aveWeight) / stdWeight)

	weightList = np.ceil((weightList - aveWeight) / stdWeight) + negBinNum
	# print(np.min(weightList), (np.max(weightList)))

	for idx, data in enumerate(dataList):
		data['colorGroup'] = int(weightList[idx])
	return dataList, int(np.max(weightList))

def getSize(dataList, key, fixSize = 5):
	if key is None:
		for data in dataList:
			data['size'] = fixSize
	else:
		for data in dataList:
			data['size'] = data[key]
	return dataList


def filterIsolatedVertex(edgeDataList, vertexDataList):
	vSet = set()
	for edge in edgeDataList:
		vSet.add(edge['source'])
		vSet.add(edge['target'])
	vertexDataList = [vertex for vertex in vertexDataList if vertex['id'] in vSet]
	return vertexDataList


if __name__ == '__main__':
	## read data
	name = 'asoiaf'
	# name = 'njals_saga'

	fileColIntList = ['source', 'target', 'value', 'layer', 'wave', 'fragment']
	# fileColIntList = ['source', 'target', 'value', 'direction', 'cycle', 'layer', 'wave', 'fragment']
	dataKeyIntList = fileColIntList

	edgeDataList = readCSV(f'dataset/preprocess/{name}_edges_decomposition.csv', fileColIntList, dataKeyIntList)

	fileColIntList = ['id', 'degree', 'peel']
	dataKeyIntList = fileColIntList
	fileColStrList = ['name']
	dataKeyStrList = fileColStrList
	fileColFloatList = ['diversity', 'betweenness', 'pagerank', 'norm_peel', 'norm_diversity', 'norm_betweenness', 'norm_pagerank']
	dataKeyFloatList = fileColFloatList

	vertexDataList = readCSV(f'dataset/preprocess/{name}_nodes_prop.csv', fileColIntList, dataKeyIntList, fileColStrList, dataKeyStrList, fileColFloatList, dataKeyFloatList)


	## filter out isolated vertices
	vertexDataList = filterIsolatedVertex(edgeDataList, vertexDataList)


	## settings of layout
	edgeColorKey = 'value'
	vertexColorKey = 'degree'
	edgeSizeKey = 'value'
	vertexSizeKey = None
	force = -300

	## prepare color
	edgeDataList, edgeMaxColor = getColorGroup(edgeDataList, edgeColorKey, bucketFlag = True)
	vertexDataList, vertexMaxColor = getColorGroup(vertexDataList, vertexColorKey, bucketFlag = True)

	## prepare size
	edgeDataList = getSize(edgeDataList, edgeSizeKey)
	vertexDataList = getSize(vertexDataList, vertexSizeKey)

	## stringfy input graph
	graph = json.dumps({'nodes': vertexDataList, 'links': edgeDataList})

	## write layout html file
	htmlFile = getHTML(graph, edgeMaxColor, vertexMaxColor, force, pageSize = 8000, showName = True)
	with open(f'./draw/{name}_vertex_{vertexSizeKey}_{vertexColorKey}_edge_{edgeSizeKey}_{edgeColorKey}.html', 'w') as file:
		file.write(htmlFile)