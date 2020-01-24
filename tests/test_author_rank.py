# imports
from AuthorRank.graph import create, export_to_json
from AuthorRank.score import top_authors
import json
import pytest


@pytest.fixture()
def sample_data() -> dict:
    """
    This fixture reads in sample data from the data directory for the purposes of testing the functionality.
    :return: None
    """

    # read in sample json
    with open("data/author_network.json", 'r') as f:
        data = json.load(f)

    return data


def test_export_format(sample_data) -> None:
    """
    Test to ensure that the graph is being effectively exported as a dictionary which is valid JSON.
    :param sample_data: the sample data
    :return: None
    """

    # generate a graph
    G = create(documents=sample_data['documents'])

    # export them
    export = export_to_json(graph=G)

    assert type(export) == dict


def test_top_author_format(sample_data) -> None:
    """
    Test to ensure that the top_author is returning a tuple of two lists with the appropriate formatting for the
    output
    :param sample_data: the sample data
    :return: None
    """

    # get the top authors for a set of documents
    top = top_authors(documents=sample_data['documents'])

    # check that it returns a tuple
    assert type(top) == tuple

    # check to ensure each value in the responses are in the appropriate format
    for k, v in zip(top[0], top[1]):
        assert type(k) == tuple
        assert type(v) == float


# TODO: test to check normalization of scores
# TODO: test to ensure the nodes and links in the graph are representative of the source document
# TODO: test to check weird formatting of input parameters
