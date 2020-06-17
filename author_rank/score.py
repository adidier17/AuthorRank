# imports
from author_rank.graph import create
from author_rank.utils import normalize
import networkx as nx
from typing import List, Tuple


def top_authors(documents: List[dict], n: int = 5, normalize_scores: bool = False, authorship_key: str = "authors", keys: set = None, progress_bar: bool = False) -> Tuple[List, List]:

    """
    Returns the top n authors according to their author_rank scores from the constructed graph as well as their scores,
    in the form of a tuple.
    :param documents: a list of dictionaries which represent documents.
    :param n: an integer to specify the number of authors to be returned.
    :param normalize_scores: a boolean to indicate whether or not to normalize the scores between 0 and 1.
    :param authorship_key: the key in the document which contains a list of dictionaries representing authors.
    :param keys: a set that contains the keys to be used to create a UID for authors.
    :param progress_bar: a boolean that indicates whether or not a progress bar should be emitted, default False.
    :return: a tuple which contains two lists, one for authors and the other for their scores.
    """

    # if keys are not provided, set a default
    # see https://florimond.dev/blog/articles/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
    if keys is None:
        keys = {"first_name", "last_name"}

    # create a directed graph that represents author relationships in the provide documents
    graph = create(documents, authorship_key=authorship_key, keys=keys, progress_bar=progress_bar)

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



