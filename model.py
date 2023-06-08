import mesa
from agent import agent
import numpy as np
import networkx as nx

def total_wealth(model):
   total=0
   for a in model.num_nodes:
      total+=a.wealth
   return total


class TrustModel(mesa.Model):
    def __init__(self, num_nodes:int): #different graphs to initialize network?
      self.seed=42
      avg_node_degree=3
      self.num_nodes = num_nodes
      prob = avg_node_degree /  num_nodes
      self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
      self.grid = mesa.space.NetworkGrid(self.G)
      self.schedule_trustee = mesa.time.RandomActivation(self)
      self.schedule_trustor = mesa.time.RandomActivation(self)
      self.datacollector = mesa.DataCollector(
        {
           "Gini": "compute_gini",
           "Wealth": "wealth",
           "Perosnalized Trust":"trust",
           "Atributes":"attributes",
        }
     )   
      for i,node in enumerate(self.G.nodes()):
            a=agent(i,self)
            if i < self.num_nodes/2:
                a.type="trustor"
                self.schedule_trustor.add(a)
            else:
                a.type="trustee"
                self.schedule_trustee.add(a)
            self.grid.place_agent(a,node_id=node)
            print(f"Agent placed: {a.id} in Node {node}" )
            print(a.type)

    #scheduler to control agent steps
    def step(self):
        pass
        #self.schedule.
        #self.datacollector.collect(self)
        # #self.schedule.step()

#random scheduler -> get list of agents by get all cell contennts of network grid