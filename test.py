import networkx as nx
import csv

import Data_manager_V0
import Environment_V0

f = open('graph_weight_test2.csv', 'w', newline='')
wr = csv.writer(f)
env = Environment_V0.LogisticNetwork()
data = Data_manager_V0.DataManager()
env.reset_network('data_road_V3.csv', 'data_hub_V3.csv')

for (d, a, wt) in env.network.edges.data('weight'):
    wr.writerow([d,a,wt])
print(nx.shortest_path(env.network, '금호JC', '포항IC', weight='weight'))
print(nx.shortest_path_length(env.network, '금호JC', '포항IC', weight='weight'))