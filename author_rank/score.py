# imports
from author_rank.utils import normalize
import networkx as nx
from typing import List, Tuple


def top_authors(graph: nx.DiGraph, n: int = 5, normalize_scores: bool = False) -> Tuple[List, List]:

    """
    Returns the top n authors according to their author_rank scores from the
    constructed graph as well as their scores, in the form of a tuple.
    :param graph: an AuthorRank graph (NetworkX DiGraph object).
    :param n: an integer to specify the number of maximum
    authors to be returned.
    :param normalize_scores: a boolean to indicate whether or not to normalize
    the scores between 0 and 1.
    :return: a tuple which contains two lists, one for authors and the other
    for their scores.
    """

    # apply the PageRank algorithm to the graph
    rank = nx.pagerank_scipy(graph)

    # sort the results
    sorted_rank = sorted(rank, key=rank.get, reverse=True)
    sorted_rank = sorted_rank[0:n]
    sorted_scores = [rank[auth] for auth in sorted_rank]

    # normalize the scores if the option is specified
    if normalize_scores:
        minimum = min(sorted_scores)
        maximum = max(sorted_scores)
        sorted_scores = [normalize(minimum, maximum, s) for s in sorted_scores]

    return sorted_rank, sorted_scores



