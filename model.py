import mesa
import agent
import numpy as np

class TrusModel(mesa.Model):
    def __init__(self, N, trust_distribution):
     self.num_agents = N
     self.trust_dst = trust_distribution
     self.schedule = mesa.time.RandomActivation(self)
     self.network = mesa.space.NetworkGrid(g=N)
     self.datacollector = mesa.DataCollector(
        model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth",
                                                                 "Perosnalized Trust":"trust",
                                                                 "Atributes":"attributes",
                                                                 "Type":"type",                                                       
                                                                 "ID":"id"}
     )   
     # Create agents
     for i in range(self.num_agents):
        for node_id in self.network.G.nodes:
            a=agent(i)
            self.network.place_agent(a,node_id=node_id)
            print(f"Agent placed: {a} in Node {node_id}" )

    #scheduler to control agent steps
    def step(self):
       self.datacollector.collect(self)
       self.schedule.step()
