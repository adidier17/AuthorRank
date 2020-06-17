from author_rank.graph import create, export_to_json
from author_rank.score import top_authors
import json

# read in mls json
with open("../data/microwave_limb_sounder.json", 'r') as f:
    # read in docs that have authors
    docs = [json.loads(d) for d in f.readlines()]
    docs = [d["_source"] for d in docs if "author" in d["_source"].keys()]
    # note cannot use json.loads as the file isn't valid JSON, each line in the file is

# subsetting to documents with a substring in the text
chlorine_partitioning_docs = [d for d in docs if "chlorine partitioning" in d["text"]]

# you can use a progress bar to indicate how far along processing is
top = top_authors(
    documents=chlorine_partitioning_docs,
    normalize_scores=True,
    n=25,
    authorship_key="author",
    keys=set(["given", "family"]),
    progress_bar=True
)

# alternatively, when a progress bar as you create a graph
G = create(
    documents=chlorine_partitioning_docs,
    authorship_key="author",
    keys=set(["given", "family"]),
    progress_bar=True
)

