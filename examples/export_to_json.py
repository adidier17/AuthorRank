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

# export them
export = ar_graph.as_json()

print(json.dumps(export, indent=4))
