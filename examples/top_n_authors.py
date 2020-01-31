# imports
from author_rank.score import top_authors
import json


# read in sample json
with open("../data/author_network.json", 'r') as f:
    data = json.load(f)

# get the top authors for a set of documents
top = top_authors(documents=data['documents'], normalize_scores=True)

# print the results
for i, j in zip(top[0], top[1]):
    print(i, j)

