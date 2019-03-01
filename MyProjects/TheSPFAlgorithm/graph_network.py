#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt

# Ориентированный граф.
G = nx.DiGraph()

G.add_nodes_from(["Pennsauken", "London", "Frankfurt", "New York", "Washington D.C.", "Paris"])

e=[("Pennsauken", "London", 315000),
   ("Pennsauken", "Frankfurt", 315000),
   ("Pennsauken", "New York", 26000),
   ("London", "Pennsauken", 315000),
   ("London", "Frankfurt", 22000),
   ("Frankfurt", "London", 22000),
   ("Frankfurt", "Pennsauken", 315000),
   ("Frankfurt", "Washington D.C.", 250000),
   ("Frankfurt", "Paris", 87000),
   ("Paris", "Frankfurt", 87000),
   ("Paris", "Washington D.C.", 600000),
   ("Washington D.C.", "Paris", 600000),
   ("Washington D.C.", "Frankfurt", 250000),
   ("Washington D.C.", "New York", 22000),
   ("New York", "Washington D.C.", 22000),
   ("New York", "Pennsauken", 26000)]
G.add_weighted_edges_from(e)

print(nx.dijkstra_path(G,"Pennsauken", "Paris"))

nx.draw(G,pos=nx.spectral_layout(G),nodecolor='r',edge_color='b',with_labels=True)
plt.savefig("graph_network.png")
plt.show()
