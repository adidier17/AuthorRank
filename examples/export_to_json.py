# imports
from author_rank.graph import create, export_to_json
import json


# read in sample json
with open("../data/author_network.json", 'r') as f:
    data = json.load(f)

# generate a graph
G = create(documents=data['documents'])

# export them
export = export_to_json(graph=G)

print(json.dumps(export, indent=4))
