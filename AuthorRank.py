from collections import Counter
import networkx as nx
import itertools



def makeGraph(badges):
	"""
	inputs: badges, list of list of strings. Each list in the list contains the badge numbers for the authors of one document. 
	outputs: G, a networkx DiGraph object
	For a given set of authors across a set of documents, this function creates a weighted graph of co-authorship. Nodes represent authors, 
	in this case using their badge numbers, and edges represent co-authorship between two authors. 
	"""
	flat_badges = list(itertools.chain.from_iterable(badges))
	counts = Counter(flat_badges)
	pairs = list(itertools.permutations(badges[0],2))
	edges_all = {}
	coAuthFrequency = {}
	for doc in badges:
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




def topNAuthors(hits, N):
	"""
	inputs: hits: a json object resulting from an elasticsearch query in the foundry tool
	N: the number of names to be displayed
	"""
	badgeNums = [doc['_source']['badgeNums'] for doc in hits if 'LDAPnames' in doc['_source'].keys() and doc['_source']['LDAPnames']]
	graph = makeGraph(query_names)
	rank = nx.pagerank_scipy(graph)
	sorted_rank = sorted(rank, key = rank.get, reverse = True)
	return(sorted_rank[0:N])