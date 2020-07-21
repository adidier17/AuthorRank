# imports
import author_rank as ar
from author_rank.utils import emit_progress_bar, normalize
import json
import os
import pytest
import random
import time


@pytest.fixture()
def sample_data() -> dict:
    """
    This fixture reads in sample data from the data directory for the purposes
    of testing the functionality.
    :return: None
    """

    # read in sample json
    with open("data/author_network.json", 'r') as f:
        data = json.load(f)

    return data


@pytest.fixture()
def mls_data() -> list:
    """
    This fixture reads in sample data from the data directory for the purposes
    of testing larger-scale data processing functions. Selects 1000 documents
    from a corpus of research papers relating to the Microwave Limb Sounder.
    :return: None
    """

    # read in sample json
    with open("data/microwave_limb_sounder.json", 'r') as f:
        # read in docs that have authors
        docs = [json.loads(d) for d in f.readlines()]
        data = [d["_source"] for d in docs if "author" in d["_source"].keys()]

    # setting a seed so that results are reproducable
    random.seed(777)

    # sample documents for testing
    random.shuffle(data)
    random_data = data[:50]

    return random_data


@pytest.fixture()
def zero_division_data() -> dict:
    """
    This fixture reads in sample data that manifests a ZeroDivisionError from
    the data directory for the purposes of
    testing the functionality under this condition.
    :return: None
    """

    # read in sample json
    with open("data/author_network_zero_division.json", 'r') as f:
        data = json.load(f)

    return data


def test_export_format(sample_data) -> None:
    """
    Test to ensure that the graph is being effectively exported as a dictionary
    which is valid JSON.
    :param sample_data: the sample data
    :return: None
    """

    # create an AuthorRank object
    ar_graph = ar.Graph()

    # fit to the data
    ar_graph.fit(
        documents=sample_data["documents"]
    )

    # export them
    export = ar_graph.as_json()

    assert type(export) == dict


def test_top_author_format(sample_data, zero_division_data) -> None:
    """
    Test to ensure that the top_author is returning a tuple of two lists with
    the appropriate formatting for the
    output
    :param sample_data: the sample data
    :return: None
    """

    # get the top authors for a set of documents
    datasets = [sample_data['documents'], zero_division_data["documents"]]

    for d in datasets:

        # create an AuthorRank object
        ar_graph = ar.Graph()

        # fit to the data
        ar_graph.fit(
            documents=d
        )

        # get the top authors for a set of documents
        top = ar_graph.top_authors()

        # check that it returns a tuple
        assert type(top) == tuple

        # check to ensure each value in the responses are in the appropriate format
        for k, v in zip(top[0], top[1]):
            assert type(k) == tuple
            assert type(v) == float


def test_normalization(sample_data) -> None:
    """
    Test to ensure that normalizing the author_rank scores returns values between
    0 and 1.
    :param sample_data: the sample data
    :return: None
    """

    # create an AuthorRank object
    ar_graph = ar.Graph()

    # fit to the data and use the progress bar
    ar_graph.fit(
        documents=sample_data['documents'],
        progress_bar=True
    )

    # get the top authors for a set of documents and normalize the scores
    top = ar_graph.top_authors(
        normalize_scores=True
    )

    # check that it returns a tuple
    assert type(top) == tuple

    # check to ensure each value in the responses are in the appropriate format
    for v in top[1]:
        assert 0. <= v <= 1.

    # check to ensure that the last entry in the list is a value of 0
    assert top[1][-1] == 0.

    # check to ensure that the first entry in the list is a value of 1
    assert top[1][0] == 1.0


def test_progress_bar_emit(sample_data) -> None:
    """
    Test to ensure that the progress bar emits the proper string under varying conditions.
    :param sample_data: the sample data
    :return: None
    """

    progress = "="

    # first, check that the progress bar emits a string
    progress_out = emit_progress_bar(progress, index=1, total=10)
    assert type(progress_out) == str

    # check that the progress bar works when the number of observations is greater / less than the terminal width
    progress_out = emit_progress_bar(progress, index=1, total=10)
    assert type(progress_out) == str

    progress_out = emit_progress_bar(progress, index=1, total=1000)
    assert type(progress_out) == str

    # next check that it returns a larger string when the index matches the block size
    # we need to override python-utils get_terminal_size to return a fixed value for testing
    os.environ["COLUMNS"] = "1000"
    progress_out = emit_progress_bar(progress, index=500, total=1000)

    assert progress_out == "=="


def test_normalization_zerodivisionerror() -> None:
    """
    Test to ensure that when authors all have the same score,
    they are all receive the same score of 1.0 after
    normalization.
    :return: None
    """

    # same scores
    scores = [25.0, 25.0, 25.0]
    minimum = min(scores)
    maximum = max(scores)

    # normalize
    top = [normalize(minimum, maximum, s) for s in scores]

    # test
    assert len(top) == 3
    for t in top:
        assert t == 1.


def test_single_author() -> None:
    """
    Tests the functionality of AuthorRank in the rare case when a single
    author is present in the document set passed.
    :return: None
    """

    # first, create a single author dataset
    data = [
        {
          "title": "PyNomaly: Anomaly detection using Local Outlier Probabilities (LoOP).",
          "authors": [
            {
              "first_name": "Valentino",
              "last_name": "Constantinou",
              "affiliation": {
                "name": "NASA Jet Propulsion Laboratory",
                "department": "Office of the Chief Information Officer"
              }
            }
          ]
        }
    ]

    # then attempt to fit to the data
    # create an AuthorRank object
    ar_graph = ar.Graph()

    with pytest.warns(UserWarning) as record:
        # fit to the data
        ar_graph.fit(
            documents=data
        )

    # check that the message matches
    messages = [i.message.args[0] for i in record]
    assert "Number of authors in document set must be greater than one. " \
           "AuthorRank not fit to the data, please try again." in messages


def test_no_fit() -> None:
    """
    Tests whether the AuthorRank approach has been fit to a set of documents
    prior to calling top_authors, and checks for the correct UserWarning.
    :return: None
    """

    # create an AuthorRank object
    ar_graph = ar.Graph()

    with pytest.warns(UserWarning) as record:
        # try to fit top authors
        ar_graph.top_authors(normalize_scores=True)

    # check that the message matches
    messages = [i.message.args[0] for i in record]
    assert "AuthorRank must first be fit on a set of documents " \
           "prior to calling top_authors." in messages


def test_speed(mls_data) -> None:
    """
    While AuthorRank is not intended to be quick, we can create a benchmark
    for its performance when generating the graph and ensure that any future
    changes to the code base do not exceed this threshold.

    This function could be used in the future to test speed improvements
    to the approach by further constraining the maximum allowed time for the
    test to pass or by testing speed differences between normal and parallel
    processing modes.

    :return: None
    """

    # get the start time
    t0 = time.time()

    # calculate the top author graph
    ar_graph = ar.Graph()
    ar_graph.fit(
        documents=mls_data,
        progress_bar=True,
        authorship_key="author",
        keys=set(["given", "family"])
    )

    # get the finish time
    t1 = time.time()

    # assert the time is less than a particular amount
    spread = t1 - t0
    assert spread < 180.

