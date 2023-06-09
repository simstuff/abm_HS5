import mesa
from .agent import agent
import numpy as np
import networkx as nx

def total_wealth(model):
   total=0
   for a in model.num_nodes:
      total+=a.wealth
   return total


class TrustModel(mesa.Model):
    def __init__(self, num_nodes:int,increase:int): #different graphs to initialize network?
      self.seed=42
      self.increase=increase
      avg_node_degree=3
      self.num_nodes = num_nodes
      prob = avg_node_degree /  num_nodes
      self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
      self.grid = mesa.space.NetworkGrid(self.G)
      self.schedule = mesa.time.BaseScheduler(self)
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
            else:
                a.type="trustee"
            self.schedule.add(a)
            self.grid.place_agent(a,node_id=node)
            print(f"Agent placed: {a.id} in Node {node}" )

    #scheduler to control agent steps
    def step(self):
        trustees = []
        trustors = []
        for i,a in enumerate(self.schedule.agent_buffer(shuffled=True)):
            if i < self.num_nodes/2:
                a.type="trustor"
                trustees.append(a)
            else:
                a.type="trustee"
                trustors.append(a)
         
        for i,a in enumerate(trustors):
            partner=trustees[i]
            a.partner=partner

        for i,a in enumerate(trustees):
            partner=trustors[i]
            a.partner=partner
            self.schedule.remove(a) #remove all trustees from schedule
            self.schedule.add(a) #add all trustees in end of schedule to execite only after action of trustors
        
         
        self.schedule.step()    

          
        #self.schedule.
        #self.datacollector.collect(self)
        # #self.schedule.step()

#random scheduler -> get list of agents by get all cell contennts of network grid