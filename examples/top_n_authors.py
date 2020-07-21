# imports
import author_rank as ar
import json


# read in sample json
with open("../data/author_network.json", 'r') as f:
    data = json.load(f)

# create an AuthorRank object
ar_graph = ar.Graph()

# fit to the data
ar_graph.fit(
    documents=data["documents"]
)

# get the top authors for a set of documents
top = ar_graph.top_authors(normalize_scores=True)

# print the results
for i, j in zip(top[0], top[1]):
    print(i, j)

