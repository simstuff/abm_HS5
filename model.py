import mesa
from agent import TrustAgent
import networkx as nx
import pandas as pd
import pickle
import sys
import matplotlib.pyplot as plt

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
    if partner is not None:
        v_list=agent.percepts[partner] 
    else:
        v_list=agent.percepts[agent.partner.unique_id] 
    return  sum(v_list)/len(v_list)
    
def get_suspectability(agent):
    return agent.suspectability

def get_id(agent):
    return agent.unique_id
    
def get_security_level(agent):
    return agent.security_level

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
    return edges
    

class TrustModel(mesa.Model):
    def __init__(self, num_nodes:int,increase:float,change_threshold:float,decrease:float,memory:int,max_step:int): #different graphs to initialize network?
        self.seed=42
        self.increase=increase
        self.decrease=decrease
        self.memory=memory
        self.change_threshold=change_threshold
        avg_node_degree=3
        self.edge_count=0
        self.step_num=0
        self.num_nodes = num_nodes
        prob = avg_node_degree /  num_nodes
        self.DG=nx.DiGraph()
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.BaseScheduler(self) #stage=interaction, step=update trust based on outcome of stage
        self.max_step=max_step

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

        #create network df
        network_data={}

        for a in self.schedule.agent_buffer(shuffled=True):
            a.wealth-=self.decrease

            #grow DiGraph for future analysis
            
            for key in a.percepts.keys():
                if self.DG.has_edge(a.unique_id,key):
                    weight=get_personalized_trust(a,partner=key)
                    info=get_info(a)      
                    self.DG[a.unique_id][key]["info"]=info
                    self.DG[a.unique_id][key].update({"weight": weight})
                else:
                    self.edge_count+=1
                    weight=get_personalized_trust(a,partner=key)
                    info=get_info(a)      
                    self.DG.add_edge(a.unique_id,key,weight=weight,info=info)
                graph_data=nx.to_dict_of_dicts(self.DG)
                with open('graph_data.pickle', 'wb') as handle:
                    pickle.dump(graph_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
                
                df1=make_edge_df(self.DG)
                df1["step"]=self.step_num
                print(df1)
                network_data.update(df1)
        df=pd.DataFrame(network_data)
        df.to_csv("graph_data.csv")
            
        self.step_num+=1
        if self.step_num > 1:  
            self.datacollector.collect(self)
            agent_data=self.datacollector.get_agent_vars_dataframe()
            model_data=self.datacollector.get_model_vars_dataframe()
            agent_data.to_csv("agent_data.csv")
            model_data.to_csv("model_data.csv")
        
        print(self.max_step)
        if self.step_num==self.max_step:
            sys.exit()      

        #if self.step_num==10:
         #   pos=nx.spring_layout(self.DG,seed=5)
          #  fig, ax = plt.subplots()
           # nx.draw(self.DG, pos)
            #edge_labels=dict([((u,v,),d['weight'])
             #   for u,v,d in self.DG.edges(data=True)])
            #nx.draw_networkx_edge_labels(self.DG, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)
            #plt.show()

#draw edge width based on personalized trust value to improve readability





