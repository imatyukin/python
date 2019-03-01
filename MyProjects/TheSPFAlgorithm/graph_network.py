#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_nodes_from(["Pennsauken", "London", "Frankfurt", "New York", "Washington D.C.", "Paris"])
G.add_edges_from([("Pennsauken", "London"),
                  ("Pennsauken", "Frankfurt"),
                  ("Pennsauken", "New York"),
                  ("London", "Pennsauken"),
                  ("London", "Frankfurt"),
                  ("Frankfurt", "London"),
                  ("Frankfurt", "Pennsauken"),
                  ("Frankfurt", "Washington D.C."),
                  ("Frankfurt", "Paris"),
                  ("Paris", "Frankfurt"),
                  ("Paris", "Washington D.C."),
                  ("Washington D.C.", "Paris"),
                  ("Washington D.C.", "Frankfurt"),
                  ("Washington D.C.", "New York"),
                  ("New York", "Washington D.C."),
                  ("New York", "Pennsauken")])

nx.draw(G,with_labels=True)
plt.savefig("graph_network.png")
plt.show()
