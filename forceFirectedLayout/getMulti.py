from collections import defaultdict

from utility import *

def getMulti(edgeList):
	multiDict = defaultdict(int)
	direcDict = defaultdict(int)
	for x, y in edgeList:
		if x < y:
			direcDict[(x, y)] += 1
			multiDict[(x, y)] += 1
		else:
			direcDict[(y, x)] -= 1
			multiDict[(y, x)] += 1
	
	multiEdgeDataList = []
	for x, y in sorted(multiDict.keys()):
		value = multiDict[(x, y)]
		direction = direcDict[(x, y)]
		cycle = (value - abs(direction)) // 2
		rowData = {'source': x, 'target': y, 'value': value, 'direction': direction, 'cycle': cycle}
		multiEdgeDataList.append(rowData)
	return multiEdgeDataList

if __name__ == '__main__':
	name = 'njals_saga'
	
	fileColIntList = ['Source', 'Target']
	dataKeyIntList = ['source', 'target']
	fileColStrList = []
	dataKeyStrList = []
	edgeDataList = readCSV(f'dataset/{name}_edges.csv', fileColIntList, dataKeyIntList, fileColStrList, dataKeyStrList)
	
	edgeList = [(edge['source'], edge['target']) for edge in edgeDataList if edge['source'] != edge['target']]
	
	multiEdgeDataList = getMulti(edgeList)

	fileColList = ['source', 'target', 'value', 'direction', 'cycle']
	writeCSVDict(f'dataset/{name}_edges_multi.csv', fileColList, multiEdgeDataList)
