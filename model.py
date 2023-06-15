import mesa
from agent import TrustAgent
#import numpy as np
import networkx as nx

def total_wealth(model):
    total=0
    for a in model.schedule.agent_buffer(shuffled=False):
      total+=a.wealth
    return total

def personalized_trust_per_agent(model):
    values={}
    for a in model.schedule.agent_buffer(shuffled=True):
        values[a.unique_id]=a.percepts
    return values

def get_gtrusting(model):
    count=0
    for a in model.schedule.agent_buffer(shuffled=True):
        if a.generalized_trust > 0:
            count+=1
    return count

def get_gmistrusting(model):
    count=0
    for a in model.schedule.agent_buffer(shuffled=True):
        if a.generalized_trust < 0:
            count+=1
    return count

def get_avg_ptrust(model):
    values=personalized_trust_per_agent(model)
    total=[]
    tmp=[]
    for val in values.values():
        for v in val:
            tmp.append(v)
        total.append(sum(tmp)/len(tmp))
    total=sum(total)/len(total)
    return total

def get_avg_gtrust(model):
    count=[]
    for a in model.schedule.agent_buffer(shuffled=True):
        count.append(a.generalized_trust)
    count=sum(count)/len(count)
    return count


class TrustModel(mesa.Model):
    def __init__(self, num_nodes:int,increase:float,change_threshold:float,decrease:float): #different graphs to initialize network?
      self.seed=42
      self.increase=increase
      self.decrease=decrease
      self.change_threshold=change_threshold
      avg_node_degree=3
      self.step_num=0
      self.num_nodes = num_nodes
      prob = avg_node_degree /  num_nodes
      self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
      self.grid = mesa.space.NetworkGrid(self.G)
      self.schedule = mesa.time.BaseScheduler(self) #stage=interaction, step=update trust based on outcome of stage

#      self.schedule = mesa.time.StagedActivation(self,["interact","step"]) #stage=interaction, step=update trust based on outcome of stage
      self.datacollector = mesa.DataCollector(
        {
           "Wealth": total_wealth,
           "PersonalizedTrust":personalized_trust_per_agent,
           "GeneralizedTrustingAgents":get_gtrusting,
           "GeneralizedMistrustingAgents":get_gmistrusting,
           "AvgPersonalizedTrust":get_avg_ptrust,
           "AvgGeneralizedTrust":get_avg_gtrust
           #"Atributes":"attributes",possible extensions
        }
     )   
      for i,node in enumerate(self.G.nodes()):
            a=TrustAgent(i,self)
            if i < self.num_nodes/2:
                a.type="trustor"
            else:
                a.type="trustee"
            self.schedule.add(a)
            self.grid.place_agent(a,node_id=node)
            print(f"Agent placed: {a.unique_id} in Node {node}" )

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
            print("Agent {} is trustor and interacting with trustee {}".format(a.unique_id,partner.unique_id))
            self.schedule.remove(a)
            self.schedule.add(a)

        for i,a in enumerate(trustees):
            partner=trustors[i]
            a.partner=partner
            self.schedule.remove(a) #remove all trustees from schedule
            self.schedule.add(a) #add all trustees in end of schedule to execite only after action of trustors
        
         
        self.schedule.step() 
        for i,a in enumerate(self.schedule.agent_buffer(shuffled=True)):
            a.wealth-=1

        self.step_num+=1  
        self.datacollector.collect(self)
