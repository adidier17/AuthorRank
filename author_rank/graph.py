# imports
from author_rank.score import top_authors as top
from author_rank.utils import emit_progress_bar, check_author_count
from collections import Counter
import itertools
import networkx as nx
from typing import List, Tuple
import warnings


class Graph:

    def __init__(self):
        self.graph = nx.DiGraph()
        self._is_fit = False

    def fit(self, documents: List[dict], authorship_key: str = "authors",
            keys: set = None, progress_bar: bool = False) -> 'nx.classes.digraph.DiGraph':

        """
        Creates a directed graph object from the list of input documents which
        are represented as dictionaries.
        :param documents: a list of dictionaries which represent documents.
        :param authorship_key: the key in the document which contains a list
        of dictionaries representing authors.
        :param keys: a set that contains the keys to be used to create a UID
        for authors.
        :param progress_bar: a boolean that indicates whether or not a progress
        bar should be emitted, default False.
        :return: a NetworkX DiGraph object.
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
        # unique combination of key values will serve as keys for each author
        flattened_list = list(itertools.chain.from_iterable(doc_authors))
        author_uid_tuples = [tuple(d.values()) for d in flattened_list]
        # ajd_matrix = np.empty(shape=())

        # get overall counts of each author
        counts = Counter(author_uid_tuples)

        acceptable_author_count = check_author_count(counts)
        if acceptable_author_count is False:
            warnings.warn("Number of authors in document set must be greater than one. "
                          "AuthorRank not fit to the data, please try again.", UserWarning)
        else:
            # create lists for the edges
            edges_all = list()

            # process each document, create the edges with the appropriate weights
            progress = "="
            for doc in range(0, len(doc_authors)):
                if len(doc_authors[doc]) > 1:
                    author_ids = [tuple(d.values()) for d in doc_authors[doc]]
                    pairs = (list(itertools.permutations(author_ids, 2)))
                    # calculate g_i_j_k
                    exclusivity = 1 / (len(doc_authors[doc]) - 1)
                    edges_all.extend([{"edge": (x[0], x[1]), "weight": exclusivity} for x in pairs])
                else:
                    edges_all.extend([{"edge": (doc_authors[doc][0], doc_authors[doc][0]), "weight": 1}])

                if progress_bar:
                    progress = emit_progress_bar(progress, doc+1, len(doc_authors))

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
                    # this occurs when an author is compared to one-self, which is
                    # not a valid scenario for the graph
                    pass

            # create the directed graph
            edge_list = [(k[0], k[1], v) for k, v in normalized.items()]
            self.graph.add_weighted_edges_from(edge_list)

            self._is_fit = True

        return self.graph

    def top_authors(self, n: int = 10, normalize_scores: bool = False) -> Tuple[List, List]:
        """
        Calculates the top N authors in an AuthorRank graph and returns them
        in sorted order.
        :param n: an integer to specify the maximum number of authors to be
        returned.
        :param normalize_scores: a boolean to indicate whether or not to normalize
        the scores between 0 and 1.
        :return: a tuple which contains two lists, one for authors and the other
        for their scores.
        """

        # check to see if AuthorRank has been fit
        if self._is_fit is False:
            warnings.warn("AuthorRank must first be fit on a set of documents "
                          "prior to calling top_authors.", UserWarning)
            return list(), list()

        else:
            top_authors, top_scores = top(self.graph, n=n, normalize_scores=normalize_scores)

            return top_authors, top_scores

    def as_json(self) -> dict:
        """
        Returns the directed graph in JSON format, containing information
        about nodes and their relationships to one another in the form of edges.
        A wrapper around the NetworkX functionality.
        :return: a JSON format for the provided graph
        """

        return nx.readwrite.json_graph.node_link_data(self.graph)

