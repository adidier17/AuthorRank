# AuthorRank
A modification of PageRank to find the most prestigious authors in a scientific collaboration network.

## Purpose
A key question in the analysis of collaborative networks is: "Who are the most prestigious authors?" Answering this question can be useful in identifying subject matter experts or in ranking search results. This module was written to determine the most prestigious authors across a research network utilizing a body or research papers, but determining prestige within a network is not confined to research collaborations and this module could be extended to other purposes. 

## Project logic
This module implements AuthorRank [1]. AuthorRank is a modification of PageRank, Google's original algorithm for ranking webpage search results. PageRank works on the idea of transferred status. The rank of a page is the sum of the ranks of
its backlinks - if a webpage has many backlinks or a few highly ranked backlinks, its rank is also
high. The algorithm works over a directed graph in which nodes are webpages and a directed edge
represents a link from one page to another. It is assumed that each node transfers its
rank evenly to all of the other nodes it connects to. Instead of webpages, AuthorRank creates a
co-authorship network that represents the structure of scientific collaborations and the status
of individual researchers. In the network, each node represents an author and each edge
represents a collaboration. Edges are bidirectional to represent the symmetric nature of
collaboration. Unlike PageRank in which each node is assumed to transfer status equally, when
considering status in a collaboration, greater status should be given to authors who frequently
coauthor together, and status should be diminished as the number of authors in a paper
increases. Thus, edges are weighted according to frequency of co-authorship and total number
of co-authors on articles according to the diagram shown below.
![Co-AuthorshipGraph](https://github.com/adidier17/AuthorRank/blob/master/Co-AuthorshipGraph.JPG)
