import mesa
import agent
import numpy as np

class TrusModel(mesa.Model):
    def __init__(self, N, trust_distribution):
     self.num_agents = N
     self.trust_dst = trust_distribution
     self.schedule = mesa.time.RandomActivation(self)
     self.network = mesa.space.NetworkGrid(N/2)
     self.datacollector = mesa.DataCollector(
        model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        )   
     # Create agents
     for i in range(self.num_agents):
        if self.trust_dst is "poisson":
            trust = np.random.poisson(lam=1)
        else:
            trust = np.random.standard_normal()
        a = agent(i, trust)
        self.network.place_agent(a,i)

    #scheduler to control agent steps
    def step(self):
       self.datacollector.collect(self)
       self.schedule.step()
