from collections import Counter
import networkx as nx
import itertools


def makeGraph(badges):
	"""
	inputs: badges, list of list of strings. Each list in the list contains the badge numbers for the authors of one document. 
=======
def makeGraph(authors):
	"""
	inputs: authors, list of list of strings. Each list in the list should contain identifying information (like names or id numbers) 
		of all authors of a paper. 
	outputs: G, a networkx DiGraph object
	For a given set of authors across a set of documents, this function creates a weighted graph of co-authorship. Nodes represent authors, 
	in this case using their badge numbers, and edges represent co-authorship between two authors. 
"""
	flat_authors = list(itertools.chain.from_iterable(authors))
	counts = Counter(flat_authors)
	pairs = list(itertools.permutations(authors[0],2))
	edges_all = {}
	coAuthFrequency = {}
	for doc in authors:
	    if len(doc) > 1:
	        pairs = (list(itertools.permutations(doc, 2)))
	        exclusivity = 1/len(doc)
	        edges = {(x[0], x[1]): exclusivity for x in pairs}   
	    else:
	        edges = {(doc[0], doc[0]): 1}
	    coAuthFrequency = {x: edges.get(x,0) + edges_all.get(x,0) for x in set(edges).union(edges_all)}    
	normalized = {key: coAuthFrequency[key]/counts[key[0]] for key in edges_all}
	edge_list = [(k[0],k[1],v)  for k,v in normalized.items()]
	G = nx.DiGraph()
	G.add_weighted_edges_from(edge_list)
	return(G)


def topNAuthors(authors, N):
	"""
	inputs: authors, list of list of strings. Each list in the list should contain identifying information (like names or id numbers) 
		of all authors of a paper. 
	N: the number of names to be displayed
	"""
	graph = makeGraph(authors)
	rank = nx.pagerank_scipy(graph)
	sorted_rank = sorted(rank, key = rank.get, reverse = True)
	return(sorted_rank[0:N])

