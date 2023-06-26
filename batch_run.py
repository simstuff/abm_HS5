import mesa
from agent import TrustAgent
import pandas as pd
import networkx as nx

#Model level data collectors

def total_wealth(model):
    total=0
    for a in model.schedule.agent_buffer(shuffled=False):
      total+=a.wealth
    return total

def personalized_trust_per_agent(model):
    values={}
    for a in model.schedule.agent_buffer(shuffled=False):
        values[a.unique_id]=a.percepts
    return values

def get_gtrusting(model):
    count=0
    for a in model.schedule.agent_buffer(shuffled=False):
        if a.generalized_trust > 0:
            count+=1
    return count

def get_gmistrusting(model):
    count=0
    for a in model.schedule.agent_buffer(shuffled=False):
        if a.generalized_trust < 0:
            count+=1
    return count

def get_avg_ptrust(model):
    values=personalized_trust_per_agent(model)
    total=[]
    tmp=[]
    if bool(values):
        for val in values.values():#get each trust dict
            for v in val.values():#get list of trust values
                tmp.append(sum(v)) 
            try:
                total.append(sum(tmp)/len(tmp))
            except ZeroDivisionError:
                print("division by zero")
        total=sum(total)/len(total)
        return total
    else:
        return 0

       
def get_avg_gtrust(model):
    count=[]
    for a in model.schedule.agent_buffer(shuffled=False):
        count.append(a.generalized_trust)
    count=sum(count)/len(count)
    return count

#Agent level data collectors

def get_wealth(agent):
    return agent.wealth

def get_info(agent):
    return agent.info

def get_generalized_trust(agent):
    return agent.generalized_trust
    
def get_personalized_trust(agent):
    return agent.percepts[agent.partner.unique_id]  
    
def get_suspectability(agent):
    return agent.suspectability

def get_id(agent):
    return agent.unique_id
    
def get_security_level(agent):
    return agent.security_level
    

class TrustModel(mesa.Model):
    def __init__(self, num_nodes:int,increase:float,change_threshold:float,decrease:float,memory:int): #different graphs to initialize network?
        self.seed=42
        self.increase=increase
        self.decrease=decrease
        self.memory=memory
        self.change_threshold=change_threshold
        avg_node_degree=3
        self.step_num=0
        self.num_nodes = num_nodes
        prob = avg_node_degree /  num_nodes
        self.MG=nx.MultiDiGraph()
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.BaseScheduler(self) #stage=interaction, step=update trust based on outcome of stage

        self.datacollector = mesa.DataCollector(model_reporters=
        {
           "TotalWealth": total_wealth,
           "GeneralizedTrustingAgents":get_gtrusting,
           "GeneralizedMistrustingAgents":get_gmistrusting,
           "AvgPersonalizedTrust":get_avg_ptrust,
           "AvgGeneralizedTrust":get_avg_gtrust
        },
        agent_reporters=
        {
            "Info":get_info,
            "PersonalizedTrust":get_personalized_trust,
            "GeneralizedTrust":get_generalized_trust,
            "Wealth":get_wealth,
            "Suspectability":get_suspectability,
            "ID":get_id,
            "SecurityLevel":get_security_level,
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
        
        self.running = True

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
            a.wealth-=self.decrease
            for key in a.percepts.keys():
                self.MG.add_edge(a.unique_id,key)
            
        self.step_num+=1
        if self.step_num > 1:  
            self.datacollector.collect(self)

    


model_params={
    "num_nodes":[10,50,100],
    "increase":[1.5,3,10],
    "change_threshold":[0.25,0.5,0.75],
    "decrease":[0,1,10],
    "memory":[1,3,10],
}
if __name__ == "__main__":
    data = mesa.batch_run(
        TrustModel,
        model_params,
        iterations=1,
        max_steps=10
    )
    br_df = pd.DataFrame(data)
    br_df.to_csv("TrustModel_Data.csv")