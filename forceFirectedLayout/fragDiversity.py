import numpy as np
from collections import defaultdict

from utility import *

if __name__ == '__main__':
	# name = 'asoiaf'
	# layerList = [1, 2, 3, 4, 5, 6, 8, 9, 13]
	# name = 'njals_saga'
	# layerList = [1, 2, 3, 4, 5, 8, 12]
	name = 'starwars'
	layerList = [1, 2, 4, 6, 7, 8]

	fileColIntList = ['source', 'target', 'layer', 'wave', 'fragment']
	dataKeyIntList = fileColIntList

	edgeDataList = readCSV(f'dataset/preprocess/{name}_edges_decomposition.csv', fileColIntList, dataKeyIntList)

	fileColIntList = ['id']
	dataKeyIntList = fileColIntList
	fileColStrList = ['name']
	dataKeyStrList = fileColStrList

	vertexDataList = readCSV(f'dataset/preprocess/{name}_nodes_prop.csv', fileColIntList, dataKeyIntList, fileColStrList, dataKeyStrList)


	for layer in layerList:
		edgeList = [edge for edge in edgeDataList if edge['layer'] == layer]

		diversityDict = dict()

		adjListDict = defaultdict(lambda: defaultdict(int))
		for edge in edgeList:
			adjListDict[edge['source']][(edge['wave'], edge['fragment'])] += 1
			adjListDict[edge['target']][(edge['wave'], edge['fragment'])] += 1

		for v, wfCountDict in adjListDict.items():
			countList = np.asarray(list(wfCountDict.values()))
			freqList = countList / np.sum(countList)
			diversity = - np.sum(freqList * np.log(freqList))
			diversityDict[v] = diversity

		for vertex in vertexDataList:
			vertex[f'f{layer}-diversity'] = diversityDict[vertex['id']] if vertex['id'] in diversityDict else 'NA'

	fileColList = ['id', 'name']
	fileColList.extend([f'f{layer}-diversity' for layer in layerList])
	writeCSVDict(f'./{name}_fragment_diversity.csv', fileColList, vertexDataList)