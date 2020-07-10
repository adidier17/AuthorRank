import author_rank as ar
import json

# read in mls json
with open("../data/microwave_limb_sounder.json", 'r') as f:
    # read in docs that have authors
    docs = [json.loads(d) for d in f.readlines()]
    docs = [d["_source"] for d in docs if "author" in d["_source"].keys()]
    # note cannot use json.loads as the file isn't valid JSON, each line in the file is

# subsetting to documents with a substring in the text
chlorine_partitioning_docs = [d for d in docs if "chlorine partitioning" in d["text"]]

# create an AuthorRank object
ar_graph = ar.Graph()

# fit to the data
ar_graph.fit(
    documents=chlorine_partitioning_docs,
    progress_bar=True, # use a progress bar to indicate how far along processing is
    authorship_key="author",
    keys=set(["given", "family"])
)

# get the top authors for a set of documents
top = ar_graph.top_authors(
    normalize_scores=True,
    n=25
)

# print the results
for i, j in zip(top[0], top[1]):
    print(i, j)


