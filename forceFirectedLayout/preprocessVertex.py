from utility import *

from alg import getPeel, getDiversity, getBetweenness, getPagerank

def filterIsolatedVertex(edgeList, peelDict, diversityDict, betweenDict, pagerankDict):
	vSet = set()
	for x, y in edgeList:
		vSet.add(x)
		vSet.add(y)

	peelDict = {key: value for key, value in peelDict.items() if key in vSet}
	diversityDict = {key: value for key, value in diversityDict.items() if key in vSet}
	betweenDict = {key: value for key, value in betweenDict.items() if key in vSet}
	pagerankDict = {key: value for key, value in pagerankDict.items() if key in vSet}
	return peelDict, diversityDict, betweenDict, pagerankDict

if __name__ == '__main__':
	## read data
	# name = 'asoiaf'
	# name = 'njals_saga'
	name = 'starwars'

	# fileColIntList = ['source', 'target', 'weight']
	# dataKeyIntList = ['source', 'target', 'value']
	# fileColIntList = ['source', 'target', 'value', 'direction', 'cycle']
	# dataKeyIntList = fileColIntList
	fileColIntList = ['source', 'target', 'frequency']
	dataKeyIntList = ['source', 'target', 'value']

	# edgeDataList = readCSV(f'dataset/{name}_edges-numbered.csv', fileColIntList, dataKeyIntList)
	# edgeDataList = readCSV(f'dataset/{name}_edges_multi.csv', fileColIntList, dataKeyIntList)
	edgeDataList = readCSV(f'dataset/{name}_edges_clean.csv', fileColIntList, dataKeyIntList)

	# fileColIntList = ['id']
	# dataKeyIntList = ['id']
	# fileColStrList = ['Label']
	# dataKeyStrList = ['name']
	# fileColIntList = ['node_id']
	# dataKeyIntList = ['id']
	# fileColStrList = ['node_label']
	# dataKeyStrList = ['name']
	fileColIntList = ['id', 'frequency']
	dataKeyIntList = ['id', 'value']
	fileColStrList = ['name']
	dataKeyStrList = ['name']

	# vertexDataList = readCSV(f'dataset/{name}_nodes-numbered.csv', fileColIntList, dataKeyIntList, fileColStrList, dataKeyStrList)
	# vertexDataList = readCSV(f'dataset/{name}_nodes.csv', fileColIntList, dataKeyIntList, fileColStrList, dataKeyStrList)
	vertexDataList = readCSV(f'dataset/{name}_nodes_clean.csv', fileColIntList, dataKeyIntList, fileColStrList, dataKeyStrList)

	## prepare input
	edgeList = [(edge['source'], edge['target']) for edge in edgeDataList if edge['source'] != edge['target']]
	edgeWeightedList = [(edge['source'], edge['target'], edge['value']) for edge in edgeDataList if edge['source'] != edge['target']]
	vertexList = [vertex['id'] for vertex in vertexDataList]

	## compute vertex property
	## peel
	peelDict, adjListDict = getPeel(edgeList)
	## diversity
	diversityDict = getDiversity(peelDict, adjListDict)
	## betweenness
	betweenDict = getBetweenness(vertexList, edgeList)
	## pagerank
	pagerankDict = getPagerank(vertexList, edgeWeightedList)


	## filter out isolated vertices
	peelDict, diversityDict, betweenDict, pagerankDict = filterIsolatedVertex(edgeList, peelDict, diversityDict, betweenDict, pagerankDict)

	## normalize
	normPeelDict = normalize(peelDict)
	normDiversityDict = normalize(diversityDict)
	normBetweenDict = normalize(betweenDict)
	normPagerankDict = normalize(pagerankDict)

	## write data
	# fileColList = ['id', 'name', 'degree', 'peel', 'diversity', 'betweenness', 'pagerank', 'norm_peel', 'norm_diversity', 'norm_betweenness', 'norm_pagerank']
	fileColList = ['id', 'name', 'value', 'degree', 'peel', 'diversity', 'betweenness', 'pagerank', 'norm_peel', 'norm_diversity', 'norm_betweenness', 'norm_pagerank']
	dataList = [(vertex['id'], vertex['name'], len(adjListDict[vertex['id']]) ,peelDict[vertex['id']], diversityDict[vertex['id']], betweenDict[vertex['id']], pagerankDict[vertex['id']], normPeelDict[vertex['id']], normDiversityDict[vertex['id']], normBetweenDict[vertex['id']], normPagerankDict[vertex['id']]) for vertex in vertexDataList if vertex['id'] in peelDict]
	writeCSVList(f'dataset/preprocess/{name}_nodes_prop.csv', fileColList, dataList)