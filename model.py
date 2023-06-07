import mesa
import agent
import numpy as np

class TrustModel(mesa.Model):
    def __init__(self, N, trust_distribution):
     self.seed=42
     self.num_agents = N
     self.schedule = mesa.time.RandomActivation(self)
     self.network = mesa.space.NetworkGrid(g=N)
     self.datacollector = mesa.DataCollector(
        model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth",
                                                                 "Perosnalized Trust":"trust",
                                                                 "Atributes":"attributes",
                                                                 "Type":"type",                                                       
                                                                 "ID":"id"}
     )   
     # Create agents128
     for i in range(self.num_agents):
        for node_id in self.network.G.nodes:
            a=agent(i,self)
            self.network.place_agent(a,node_id=node_id)
            a.neighbors=self.network.get_neighbors(node_id=i, include_center: bool = False, radius: int = 1)

            self.schedule.add(a)
            print(f"Agent placed: {a} in Node {node_id}" )

    #scheduler to control agent steps
    def step(self):
       #self.datacollector.collect(self)
       self.schedule
       self.network.get_neighbors(node_id: int, include_center: bool = False, radius: int = 1)
       self.schedule.step()

#random scheduler -> get list of agents by get all cell contennts of network grid