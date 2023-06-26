import mesa
import numpy as np
from math import fsum

class TrustAgent(mesa.Agent):
    def __init__(self, id:int,model):
        super().__init__(id,model)
        self.generalized_trust=np.random.normal(loc=0.0,scale=0.5,size=None)
        self.wealth=np.random.uniform(low=1,high=10) #pareto distribution for wealth
        self.type=None
        self.send_money=False
        self.info=0 #sum of info from neighbors
        self.suspectability=np.random.uniform(low=0,high=1.0)
        self.percepts={}
        self.last_wealth=None
        self.model=model
        self.partner=None
        self.neighbors=[] #to be initialized through grid
        self.memory=[]#sum all elements in array and if 3 then change generlaized trust
        self.security_level=np.random.uniform(low=1,high=1.5)
        self.memory_span=np.random.uniform(low=1,high=self.model.memory) #draw from prob dstr

    def step(self):
        if self.last_wealth is not None: #to not execute check in first round
            self.check_wealth_update_trust()
        self.last_wealth=self.wealth
        self.interact()


    def interact(self):
        self.calculate_neighbor_info()
        trust_level=self.calculate_trust() #believe
        self.last_wealth=self.wealth

        if self.type=="trustor":
            print("trustor acts")
            if self.wealth > self.security_level*trust_level: #desire
                self.partner.wealth+=self.model.increase #intention
                print("increased wealth")
            
        else:
            print("trustee acts")
            if self.wealth > self.security_level*trust_level: #desire
                self.partner.wealth+=self.model.increase/2 #intention
                self.wealth-=self.model.increase/2
                print("decreased wealth")

        if len(self.memory) > self.model.memory:
            if sum(self.memory[-self.model.memory:])==self.model.memory:
                change_prop=np.random.uniform()
                if change_prop > self.model.change_threshold: #zufällige Wsl für Änderung von generalized trust
                    self.generalized_trust=self.generalized_trust+self.generalized_trust*change_prop
                    self.generalized_trust=self.center(self.generalized_trust)

                if sum(self.memory[-self.model.memory:])==0:
                    change_prop=np.random.uniform()
                    if change_prop < self.model.change_threshold: #zufällige Wsl für Änderung von generalized trust
                        self.generalized_trust=self.generalized_trust+self.generalized_trust*-1*change_prop
                        self.generalized_trust=self.center(self.generalized_trust)

       


    #trust should be expressed as percentage to enable gradual sendings, send =1*trust, if < 0.5 no trust
    def calculate_trust(self):
        if self.partner.unique_id in self.percepts:
            personalized_trust=self.percepts.get(self.partner.unique_id)
            if isinstance(personalized_trust,list):
                personalized_trust=fsum(personalized_trust)/len(personalized_trust)
            trust_level=(((self.generalized_trust+personalized_trust)/2)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust+personalized_trust)/2

        else:
            if self.info==0:
                trust_level=self.generalized_trust
            else:
                trust_level=((self.generalized_trust)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust)
                
        return trust_level

    def calculate_neighbor_info(self):
        self.info=0
        self.neighbors=self.model.grid.get_neighbors(node_id=self.unique_id, include_center=False,radius=1)
        
        for n in self.neighbors:
            if n in self.percepts:
                    weight=self.percepts[n]
            else:
                weight=self.generalized_trust
            
            for a in self.model.schedule.agent_buffer(shuffled=False):
                if a.unique_id in self.neighbors:
                    if self.partner in a.percepts and self.partner is not None:
                        self.info+=fsum(a.percepts[self.partner.unique_id])*weight
        

        if self.info > 0:
            self.info=self.info/len(self.neighbors) #averages info

    def check_wealth_update_trust(self):
        change=np.random.uniform() 
        #get last_trust_values
        if self.partner.unique_id in self.percepts:
            last_trust_value=self.percepts.get(self.partner.unique_id)
            print("--id--",last_trust_value)
        else: #include forgetting through if len(last_tr_v)>5: last_trsut_v[-1]= else append
            last_trust_value=self.generalized_trust
            last_trust_value=list([float(last_trust_value)])

        trust_value=fsum(last_trust_value)/len(last_trust_value)        

        if self.last_wealth > self.wealth: 
            new_trust_value=trust_value-change*trust_value
            self.center(new_trust_value)
            last_trust_value.append(new_trust_value)
            self.percepts[self.partner.unique_id]=last_trust_value
            self.memory.append(0)
            print("Reduced trust")
        
        else:
            new_trust_value=trust_value+change*trust_value
            self.center(new_trust_value)
            last_trust_value.append(new_trust_value)
            self.percepts[self.partner.unique_id]=last_trust_value
            self.memory.append(1)
            print("Increased trust")

    def center(self,x): #keep values between -1 and 1
        if x>=0:
            x=min(1,x)
        else:
            x=max(-1,x)
        return x
