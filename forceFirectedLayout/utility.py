import csv
from collections import defaultdict

## general

# [(x, y)] -> [(x, y), (y, x)]
def getSimpleUndirected(edgeList):
	dirEdgeSet = {(x, y) for (x, y) in edgeList if x != y}
	revEdgeSet = {(y, x) for (x, y) in dirEdgeSet}
	return list(dirEdgeSet | revEdgeSet)

# [(x, y)] -> {x: [y]}
def getAdjList(edgeSet):
	adjListDict = defaultdict(list)
	for x, y in edgeSet:
		adjListDict[x].append(y)
	return adjListDict

# {key: value}, where value in [0, inf) -> {key: value_normalized}, where value_normalized in [0, 1]
def normalize(dataDict):
	maxData = max(dataDict.values())
	dataDict = {key: value / maxData for key, value in dataDict.items()}
	return dataDict


## I/O

# 'fileColInt, fileColStr, fileColFloat' -> {dataKeyInt: int(fieColInt), dataKeyStr: fileColStr, dataKeyFloat: float(fileColFloat)}
def readCSV(fileName, fileColIntList, dataKeyIntList, fileColStrList = None, dataKeyStrList = None, fileColFloatList = None, dataKeyFloatList = None):
	fileColStrList = [] if fileColStrList is None else fileColStrList
	dataKeyStrList = [] if dataKeyStrList is None else dataKeyStrList
	fileColFloatList = [] if fileColFloatList is None else fileColFloatList
	dataKeyFloatList = [] if dataKeyFloatList is None else dataKeyFloatList

	with open(fileName, 'r') as file:
		reader = csv.DictReader(file)
		data = []
		for row in reader:
			rowData = dict()
			for col, key in zip(fileColIntList, dataKeyIntList):
				rowData[key] = int(row[col])
			for col, key in zip(fileColStrList, dataKeyStrList):
				rowData[key] = row[col]
			for col, key in zip(fileColFloatList, dataKeyFloatList):
				rowData[key] = float(row[col])
			data.append(rowData)
	return data

# [(value)] -> 'value'
def writeCSVList(fileName, fileColList, data):
	with open(fileName, 'w', newline = '') as file:
		writer = csv.writer(file)
		writer.writerow(fileColList)
		for rowData in data:
			writer.writerow(rowData)
	return

# [{fileCol: value}] -> 'value'
def writeCSVDict(fileName, fileColList, data):
	with open(fileName, 'w', newline = '') as file:
		writer = csv.DictWriter(file, fileColList)
		writer.writeheader()
		for rowData in data:
			writer.writerow(rowData)
	return