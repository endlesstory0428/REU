import numpy as np
import networkx as nx

from utility import *

## k-core updating

class core(object):
	def __init__(self, adjListDict):
		super(core, self).__init__()
		self.adjListDict = adjListDict.copy()
		return

	def getDegree(self):
		degreeDict = dict()
		for v, neighborList in self.adjListDict.items():
			d = len(neighborList)
			degreeDict[v] = d
		return degreeDict

	def initTempCore(self, degreeDict = None):
		self.layerDict = dict()
		self.edgeLayerDict = dict()
		self.tempCoreDict = self.getDegree() if degreeDict is None else degreeDict
		self.messageList = [(u, self.tempCoreDict[v], float('inf')) for v, neighborList in self.adjListDict.items() for u in neighborList ]
		return self.tempCoreDict 

	def update(self, v):
		tempNeighborList = self.adjListDict[v]
		prevCore = self.tempCoreDict[v]
		for tryCore in range(prevCore + 1):
			tempNeighborList = [u for u in tempNeighborList if self.tempCoreDict[u] >= tryCore]
			if len(tempNeighborList) < tryCore:
				self.tempCoreDict[v] = tryCore - 1
				return True, prevCore
		else:
			return False, prevCore
		return

	def sendMessage(self, v, prevCore):
		for u in self.adjListDict[v]:
			self.messageList.append((u, self.tempCoreDict[v], prevCore))
		return 

	def recvMessage(self, message):
		v, tempNeighborCore, prevNeighborCore = message
		if prevNeighborCore >= self.tempCoreDict[v] > tempNeighborCore:
			updateFlag, prevCore = self.update(v)
			if updateFlag:
				self.sendMessage(v, prevCore)
		return

	def getCore(self):
		while self.messageList:
			message = self.messageList.pop()
			self.recvMessage(message)
		return self.tempCoreDict

	def filterMaxCore(self):
		maxCore = 0
		maxCoreList = []
		for v, core in self.tempCoreDict.items():
			if core > maxCore:
				maxCore = core
				maxCoreList = [v]
			elif core == maxCore:
				maxCoreList.append(v)

		for v in maxCoreList:
			self.layerDict[v] = maxCore
			newAdjList = []
			coreEdgeList = []
			for u in self.adjListDict[v]:
				if self.tempCoreDict[u] < maxCore:
					newAdjList.append(u)
				elif self.tempCoreDict[u] == maxCore:
					coreEdgeList.append(u)
				else:
					print('E: filterMaxCore', u, v)
			for u in coreEdgeList:
				self.edgeLayerDict[(v, u)] = maxCore
			self.adjListDict[v] = newAdjList

		for v in maxCoreList:
			updateFlag, prevCore = self.update(v)
			if updateFlag:
				self.sendMessage(v, prevCore)
			else:
				print('E: filterMaxCore', v)

		for v in maxCoreList:
			if not self.adjListDict[v]:
				self.adjListDict.pop(v)
		return maxCore

	def getLayer(self):
		self.initTempCore()
		while self.adjListDict:
			self.getCore()
			tempMaxCore = self.filterMaxCore()
			# tempTime1 = time.time()
			# print(tempMaxCore, tempTime1 - tempTime0)
			# tempTime0 = time.time()
		return self.tempCoreDict


## wave\fragment decomposition

def getEdgeDict(edgeLayerDict):
	edgeWaveDict = dict()
	edgeFragDict = dict()

	layerSet = set(edgeLayerDict.values())
	for layer in layerSet:
		edgeList = [edge for edge, layerIdx in edgeLayerDict.items() if layerIdx == layer]
		print(layer, len(edgeList))
		adjListDict = getAdjList(edgeList)
		wave = 0
		frag = 1
		
		while adjListDict:
			degreeDict = {v: len(neighborList) for v, neighborList in adjListDict.items()}
			minDegree = min(set(degreeDict.values()))
			if minDegree == layer:
				wave += 1
				frag = 1
			else:
				frag += 1

			for v, neighborList in adjListDict.items():
				if degreeDict[v] == minDegree:
					for u in neighborList:
						edgeWaveDict[(v, u)] = wave
						edgeFragDict[(v, u)] = frag
					adjListDict[v] = []
				else:
					newAdjList = []
					for u in neighborList:
						if degreeDict[u] == minDegree:
							edgeWaveDict[(v, u)] = wave
							edgeFragDict[(v, u)] = frag
						else:
							newAdjList.append(u)
					adjListDict[v] = newAdjList
			adjListDict = {v: neighborList for v, neighborList in adjListDict.items() if neighborList}

	return edgeWaveDict, edgeFragDict


## interface

# [(x, y)] -> {(x, y): fixpoint}, {(x, y): wave}, {(x, y): fragment}
def getDecomposition(edgeList):
	# preprocess
	edgeList = getSimpleUndirected(edgeList)
	adjListDict = getAdjList(edgeList)
	# fixpoint decompostion
	c = core(adjListDict)
	c.getLayer()
	# wave\fragment decomposition
	edgeWaveDict, edgeFragDict = getEdgeDict(c.edgeLayerDict)
	return c.edgeLayerDict, edgeWaveDict, edgeFragDict


# [(x, y)] -> {x: peel, y: peel}, {x: [y], y:[x]}
def getPeel(edgeList):
	# preprocess
	edgeList = getSimpleUndirected(edgeList)
	adjListDict = getAdjList(edgeList)
	# peel
	c = core(adjListDict)
	c.initTempCore()
	peelDict = c.getCore()
	return peelDict, adjListDict

# {v: peel}, {v: [neighbor]} -> {v: diversity}
def getDiversity(peelDict, adjListDict):
	maxCore = max(list(peelDict.values()))
	diversityDict = dict()

	for vertex in peelDict.keys():
		peelBins = np.zeros(maxCore + 1, dtype = np.float64)
		for neighbor in adjListDict[vertex]:
			peelBins[peelDict[neighbor]] += 1
		peelBins = peelBins[np.nonzero(peelBins)]
		peelBins = peelBins / np.sum(peelBins)
		diversityDict[vertex] = -np.sum(peelBins * np.log(peelBins))
	return diversityDict

# [v], [(x, y)] -> {v: betweenness}
def getBetweenness(vertexList, edgeList):
	G = nx.Graph()
	G.add_nodes_from(vertexList)
	G.add_edges_from(edgeList)
	return nx.betweenness_centrality(G)

# [v], [(x, y, w)] -> {v: pagerank}
def getPagerank(vertexList, weightedEdgeList):
	G = nx.Graph()
	G.add_nodes_from(vertexList)
	G.add_weighted_edges_from(weightedEdgeList)
	return nx.pagerank(G)