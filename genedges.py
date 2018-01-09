import networkx as nx
from constModu import *
G = nx.random_graphs.newman_watts_strogatz_graph(50, 4, 0.3)
with open(modelname + "_edges.csv", 'w') as f:
    f.write("e1,e1\n")
    for edge in G.edges():
        f.write("%d,%d\n" % (edge[0], edge[1]))
