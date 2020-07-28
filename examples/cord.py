import author_rank as ar
import json
import pandas as pd
import random


# read in the data
cord_df = pd.read_csv("../data/CORD-19/2020-07-16/metadata.csv", low_memory=False)
cord_df_search = cord_df[cord_df["title"].astype(str).str.contains("bronchiolitis")]
authors_by_document = cord_df_search["authors"].astype(str).apply(
    lambda row: [r.strip() for r in row.split(";")]
)

documents = list()
for doc in authors_by_document:
    doc_dict = {
        "authors": list()
    }
    for auth in doc:
        doc_dict["authors"].append(
            {"name": auth} # cord 19 has full name as represented on document
        )
    documents.append(doc_dict)


# create an AuthorRank object
ar_graph = ar.Graph()

# fit to the data
ar_graph.fit(
    documents=random.sample(documents, 5), # limit to small number of documents
    progress_bar=True, # use a progress bar to indicate how far along processing is
    authorship_key="authors",
    keys=set(["name"])
)

# get the top authors for a set of documents
top = ar_graph.top_authors(
    normalize_scores=True,
    n=10
)

# print the results
for i, j in zip(top[0], top[1]):
    print(i, j)

# export the data
G_json = ar_graph.as_json()
with open("../visualization/data/cord_graph.json", 'w') as f_out:
    json.dump(G_json, f_out)

scores_json = dict()
for t in zip(top[0], top[1]):
    scores_json[" ".join(t[0])] = t[1]
with open("../visualization/data/cord_scores.json", 'w') as f_out:
    json.dump(scores_json, f_out)

