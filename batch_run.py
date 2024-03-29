import mesa
from agent import TrustAgent
import networkx as nx
import pandas as pd

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
    
def get_personalized_trust(agent,partner=None):
    if partner in agent.percepts:
        v_list=sum(agent.percepts[partner])/len(agent.percepts[partner]) #weightened -> each step in the list gets cut in half or alternatively each position gets divided by length
    else:
        v_list=0
    return  v_list
    
def get_suspectability(agent):
    return agent.suspectability

def get_id(agent):
    return agent.unique_id
    
def get_security_level(agent):
    return agent.security_level

def get_num_nodes(model):
    return model.G.number_of_nodes()

#Make df from edges to store in csv
def make_edge_df(G):
    edges = {}
    for source, target, attribute in G.edges(data=True):

        if not edges.get('source'):
            edges['source'] = [source]
        else:
            edges['source'].append(source)

        if not edges.get('target'):
            edges['target'] = [target]
        else:
            edges['target'].append(target)

        for key, value in attribute.items():
            if not edges.get(key):
                edges[key] = [value]
            else:
                edges[key].append(value)
    return pd.DataFrame(edges)
    

class TrustModel(mesa.Model):
    def __init__(self, num_nodes:int,increase:float,change_threshold:float,decrease:float,memory:int):
        self.seed=42
        self.increase=increase
        self.decrease=decrease
        self.memory=memory
        self.change_threshold=change_threshold
        self.edge_count=0
        self.step_num=0
        self.num_nodes = num_nodes
        self.G=nx.DiGraph()
        self.schedule = mesa.time.BaseScheduler(self) 
        self.running=None

        self.datacollector = mesa.DataCollector(model_reporters=
        {
           "TotalWealth": total_wealth,
           "GeneralizedTrustingAgents":get_gtrusting,
           "GeneralizedMistrustingAgents":get_gmistrusting,
           "AvgPersonalizedTrust":get_avg_ptrust,
           "AvgGeneralizedTrust":get_avg_gtrust,
           "NumberOfNodes":get_num_nodes
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

        for i in range(self.num_nodes):
            a=TrustAgent(i,self)
            if i < self.num_nodes/2:
                a.type="trustor"
            else:
                a.type="trustee"
            self.schedule.add(a)
            self.G.add_node(a.unique_id)
        print(self.G)
    #scheduler to control agent steps
    def step(self):
        trustees = []
        trustors = []
        for i,a in enumerate(self.schedule.agent_buffer(shuffled=True)):
            if i < self.num_nodes/2:
                a.type="trustor"
                trustors.append(a)
            else:
                a.type="trustee"
                trustees.append(a)

        for i,a in enumerate(trustors):
            partner=trustees[i]
            a.partner=partner
            if self.G.has_edge(a.unique_id,partner.unique_id):
                weight=get_personalized_trust(a,partner=partner.unique_id)
                info=get_info(a)      
                self.G[a.unique_id][partner.unique_id].update({"info":info})
                self.G[a.unique_id][partner.unique_id].update({"weight": weight})
            else:
                weight=get_personalized_trust(a,partner=partner.unique_id)
                info=get_info(a)      
                self.G.add_edge(a.unique_id,partner.unique_id,weight=weight,info=info)
            print("Agent {} is trustor and interacting with trustee {}".format(a.unique_id,partner.unique_id))
            self.schedule.remove(a)
            self.schedule.add(a)
        
        for i,a in enumerate(trustees):
            partner=trustors[i]
            a.partner=partner
            if self.G.has_edge(a.unique_id,partner.unique_id):
                weight=get_personalized_trust(a,partner=partner.unique_id)
                info=get_info(a)      
                self.G[a.unique_id][partner.unique_id].update({"info":info})
                self.G[a.unique_id][partner.unique_id].update({"weight": weight})
            else:
                weight=get_personalized_trust(a,partner=partner.unique_id)
                info=get_info(a)      
                self.G.add_edge(a.unique_id,partner.unique_id,weight=weight,info=info)
            self.schedule.remove(a) #remove all trustees from schedule
            self.schedule.add(a) #add all trustees in end of schedule to execite only after action of trustors
         
        
        print(self.G)
        
        self.schedule.step() 


        for a in self.schedule.agent_buffer(shuffled=True):
            a.wealth-=self.decrease
            #if a.wealth<0:
                #self.G.remove_node(a.unique_id)
                #self.schedule.remove(a)

            #grow DiGraph for future analysis

            df=make_edge_df(self.G)
            df["step"]=self.step_num
            path="graphs/"+str(self.step_num)+"_graph_data"+".csv"
            df.to_csv(path)

                #safe in picke file
                #graph_data=nx.to_numpy_array(self.DG)
                #path="pickled_graphs/graph_data_"+str(self.step_num)+".pickle"
                #with open(path, 'wb') as handle:
                #    pickle.dump(graph_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        self.step_num+=1
        if self.step_num > 1:  
            self.datacollector.collect(self)
            agent_data=self.datacollector.get_agent_vars_dataframe()
            model_data=self.datacollector.get_model_vars_dataframe()
            agent_data.to_csv("agent_data.csv")
            model_data.to_csv("model_data.csv")

    


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
        max_steps=10,
        data_collection_period=-1
    )
    br_df = pd.DataFrame(data)
    br_df.to_csv("TrustModel_Data.csv")