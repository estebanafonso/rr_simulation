import networkx as nx
import matplotlib.pyplot as plt

RRG=nx.Graph()

cities = ["SEA","LA","CHI","DAL","NY","MIA"]

railways = [("SEA","CHI",{'distance':31}),
    ("CHI","NY",{'distance':12}),("CHI","DAL",{'distance':14}),
    ("DAL","MIA",{'distance':19}),("DAL","LA",{'distance':21})]
    
RRG.add_nodes_from(cities)
RRG.add_edges_from(railways)
    
nx.draw(RRG)
plt.show(RRG)