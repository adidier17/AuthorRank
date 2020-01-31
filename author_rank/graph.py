# imports
from collections import Counter
import itertools
import networkx as nx
from typing import List


def create(documents: List[dict], authorship_key: str = "authors", keys: set = None) -> 'nx.classes.digraph.DiGraph':

    """
    Creates a directed graph object from the list of input documents which are represented as dictionaries.
    :param documents: a list of dictionaries which represent documents.
    :param authorship_key: the key in the document which contains a list of dictionaries representing authors.
    :param keys: a set that contains the keys to be used to create a UID for authors.
    :return: a networkx DiGraph object.
    """

    # if keys are not provided, set a default
    # see https://florimond.dev/blog/articles/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
    if keys is None:
        keys = {"first_name", "last_name"}

    # get the authorship from each of the documents
    # gets a list of lists
    doc_authors = [i[authorship_key] for i in documents]

    # remove keys and values that are not used as part of an author UID
    for doc in doc_authors:
        for author in doc:
            unwanted_keys = set(author) - set(keys)
            for unwanted_key in unwanted_keys:
                del author[unwanted_key]

    # create a UID for each author based on the remaining keys
    # each unique combination of key values will serve as keys for each author
    flattened_list = list(itertools.chain.from_iterable(doc_authors))
    author_uid_tuples = [tuple(d.values()) for d in flattened_list]

    # get overall counts of each author
    counts = Counter(author_uid_tuples)

    # create lists for the edges
    edges_all = list()

    # process each document and create the edges with the appropriate weights
    for doc in doc_authors:
        if len(doc) > 1:
            author_ids = [tuple(d.values()) for d in flattened_list]
            pairs = (list(itertools.permutations(author_ids, 2)))
            # calculate g_i_j_k
            exclusivity = 1 / (len(doc) - 1)
            edges_all.extend([{"edge": (x[0], x[1]), "weight": exclusivity} for x in pairs])
        else:
            edges_all.extend([{"edge": (doc[0], doc[0]), "weight": 1}])

    # sort the edges for processing
    edges_all_sorted = sorted(edges_all, key=lambda x: str(x["edge"]))
    gb_object = itertools.groupby(edges_all_sorted, key=lambda x: x["edge"])

    # normalize the edge weights and create the directed graph
    normalized = {}
    for k, v in gb_object:
        try:
            v = list(v) # need to reassign
            numerator = sum(d["weight"] for d in list(v))
            denominator = counts[k[0]]
            normalized[k] = numerator / denominator
        except TypeError:
            # this occurs when an author is compared to one-self, which is not a valid scenario for the graph
            pass

    # create the directed graph
    edge_list = [(k[0], k[1], v) for k, v in normalized.items()]
    G = nx.DiGraph()
    G.add_weighted_edges_from(edge_list)

    return G


def export_to_json(graph: 'nx.classes.digraph.DiGraph'):

    """
    Returns the directed graph in JSON format, containing information
    about nodes and their relationships to one another in the form of edges.
    A wrapper around the NetworkX functionality.
    :param graph: a networkx.DiGraph object
    :return: a JSON format for the provided graph
    """

    return nx.readwrite.json_graph.node_link_data(graph)

