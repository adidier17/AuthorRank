# imports
from author_rank.score import top_authors as top
from author_rank.utils import emit_progress_bar, check_author_count
from collections import Counter
import copy
import itertools
import networkx as nx
from typing import List, Tuple
import warnings


class Graph:

    def __init__(self):
        self.graph = nx.DiGraph()
        self._is_fit = False
        self._progress = "="
        self._edges_all = list()
        self._normalized = dict()
        self._author_list = list()
        self._counter = 0
        self._gb_object_len = 0

    def _extend_graph(self, authors_by_document: list, doc_index: int, progress_bar: bool) -> list:
        """
        Creates the AuthorRank graph based on the relationships between the
        authors and returns the created edges.
        :param authors_by_document: a list of lists - a list of authors by document.
        :param doc_index: the integer position of the document to be processed.
        :param progress_bar: a boolean indicating whether or not to use the progress bar.
        :return: a list of edges based on the document's authorship.
        """

        edge = None
        if len(authors_by_document[doc_index]) > 1:
            # author_ids = [tuple(d.values()) for d in self._author_list]
            pairs = (list(itertools.permutations(authors_by_document[doc_index], 2)))
            # calculate g_i_j_k
            exclusivity = 1 / (len(authors_by_document[doc_index]) - 1)
            edge = [{"edge": (x[0], x[1]), "weight": exclusivity} for x in pairs]
        elif len(authors_by_document[doc_index]) == 1:
            edge = [{"edge": (authors_by_document[doc_index][0], authors_by_document[doc_index][0]), "weight": 1}]

        if edge is not None:
            self._edges_all.extend(edge)

        if progress_bar:
            self._progress = emit_progress_bar(self._progress, doc_index + 1, int(len(authors_by_document) * 2.))

        return edge

    def _weigh_graph(self, groupby: itertools.groupby, progress_bar: bool, author_counts: Counter) -> None:
        """
        Weighs the edges in the AuthorRank graph according to the approach outlined in the paper and
        updates a normalization dictionary.
        :param groupby: An itertools.groupby object.
        :param progress_bar: a boolean indicating whether or not to use the progress bar.
        :param author_counts: A collections Counter object that provides the document counts
        for each author.
        :return: None
        """

        # normalize the edge weights and create the directed graph
        v = groupby[1]
        k = groupby[0]
        try:
            v = list(v)  # need to reassign
            numerator = sum(d["weight"] for d in list(v))
            denominator = author_counts[k[0]]
            self._normalized[k] = numerator / denominator
        except TypeError:
            # this occurs when an author is compared to one-self, which is
            # not a valid scenario for the graph
            pass

        if progress_bar:
            self._progress = emit_progress_bar(self._progress, self._counter, self._gb_object_len, percent_offset=0.5)

        self._counter += 1

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
        doc_authors_tuples = [[tuple(d.values()) for d in doc] for doc in doc_authors]
        # unique combination of key values will serve as keys for each author
        # self._author_list = list(itertools.chain.from_iterable(doc_authors))

        # author_uid_tuples = [tuple(d.values()) for d in self._author_list]
        # get overall counts of each author
        author_list = list(itertools.chain.from_iterable(doc_authors_tuples))
        counts = Counter(author_list)
        acceptable_author_count = check_author_count(counts)
        if acceptable_author_count is False:
            warnings.warn("Number of authors in document set must be greater than one. "
                          "AuthorRank not fit to the data, please try again.", UserWarning)
        else:
            # process each document, create the edges with the appropriate weights
            for doc in range(0, len(doc_authors)):
                self._extend_graph(doc_authors_tuples, doc, progress_bar)

            # sort the edges for processing
            edges_all_sorted = sorted(self._edges_all, key=lambda x: str(x["edge"]))
            gb_object = itertools.groupby(edges_all_sorted, key=lambda x: x["edge"])

            self._counter = 0
            self._gb_object_len = sum(1 for x in copy.deepcopy(gb_object))

            for k, v in gb_object:
                self._weigh_graph((k, v), progress_bar, counts)

            # create the directed graph
            edge_list = [(k[0], k[1], v) for k, v in self._normalized.items()]
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

