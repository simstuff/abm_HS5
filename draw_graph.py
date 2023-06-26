import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("graph_data.csv")
#G=nx.from_pandas_edgelist(df)

import pickle

with open('graph_data.pickle', 'rb') as handle:
    data = pickle.load(handle)

G=nx.from_dict_of_dicts(data)
#G=G.to_directed()
pos=nx.spring_layout(G)
subax1 = plt.subplot(121)
#nx.draw(G, with_labels=True, font_weight='bold')

#nx.draw_networkx(G,pos=pos,arrows=True,with_labels=True,connectionstyle='arc3, rad = 0.1')
#plt.show() 

pos=nx.spring_layout(G,seed=5)
fig, ax = plt.subplots()
nx.draw(G, pos)
edge_labels=dict([((u,v,),d['weight'])
    for u,v,d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)
plt.show()