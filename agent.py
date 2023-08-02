import mesa
import numpy as np
from math import fsum

class TrustAgent(mesa.Agent):
    def __init__(self, id:int,model):
        super().__init__(id,model)
        self.generalized_trust=np.random.normal(loc=0.0,scale=0.5,size=None)
        self.wealth=np.random.pareto(a=5.) #pareto distribution for wealth
        self.change_threshold=np.random.uniform(low=0.1,high=1.0) #threshold for change of generalized trust
        self.type="" #trustor or trustee
        self.info=0 #info from neighbors
        self.suspectability=np.random.normal(loc=0.5,scale=0.5,size=None) 
        self.percepts={} #memory of past interactions with exact trust values
        self.last_wealth=self.wealth 
        self.model=model 
        self.partner=None #interaction partner for round
        self.neighbors=[] 
        self.memory=[]#memory of positive or negative interaction, no exact trust values
        self.security_level=np.random.normal(loc=5,scale=5,size=None) #security level to calculate final trust level 
        self.memory_span=np.random.randint(low=2,high=10) #number of positive or negative interactions inducing change of generalized trust

    def step(self):
        self.check_wealth_update_trust()
        self.interact()


    def interact(self):
        self.calculate_neighbor_info()
        trust_level=self.calculate_trust() #believe
        
        #check type and then act accordingly to type
        if self.type=="trustor":
            if self.wealth > self.security_level*trust_level: #desire (BDI)
                self.partner.wealth+=self.model.increase #intention (BDI)
            
        else:
            if self.wealth>self.last_wealth:
                if self.wealth > self.security_level*trust_level: #desire (BDI)
                    self.partner.wealth+=(self.wealth-self.last_wealth)/2 #intention (BDI)
                    self.wealth-=(self.wealth-self.last_wealth)/2

        #check if generalized trust needs to change
        if len(self.memory) > self.memory_span:
            if sum(self.memory[-self.memory_span:])==self.memory_span:
                change_prop=np.random.uniform()
                if change_prop > self.change_threshold: #zufällige Wsl für Änderung von generalized trust
                    self.generalized_trust=self.generalized_trust+self.generalized_trust*change_prop
                    self.generalized_trust=self.center(self.generalized_trust)

                if sum(self.memory[-self.memory_span:])==0:
                    change_prop=np.random.uniform()
                    if change_prop < self.change_threshold: #zufällige Wsl für Änderung von generalized trust
                        self.generalized_trust=self.generalized_trust+self.generalized_trust*-1*change_prop
                        self.generalized_trust=self.center(self.generalized_trust)

       

    #calculate trust value
    def calculate_trust(self):
        if self.partner.unique_id in self.percepts:
            trust_list=self.percepts.get(self.partner.unique_id)
            personalized_trust=0.
            if isinstance(trust_list,list):
                for i,p in enumerate(trust_list):
                    personalized_trust+=(1/(len(trust_list)-i))*p
            personalized_trust=personalized_trust/len(trust_list)
            trust_level=(((self.generalized_trust+personalized_trust)/2)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust+personalized_trust)/2
            #calculate through formula of social influence network theory
        else:
            if self.info==0:
                trust_level=self.generalized_trust
            else:
                trust_level=((self.generalized_trust)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust)
                
        return trust_level

    def calculate_neighbor_info(self):
        self.info=0
        self.neighbors=self.model.G.neighbors(self.unique_id)
        k=0
        #check if neighbor has been interacted with, otherwise use generalized trust as weight 
        for n in self.neighbors:
            if n in self.percepts:
                summed_percepts1=0.
                for i, p in enumerate(self.percepts[n]):
                    summed_percepts1+=(1/(len(self.percepts[n])-i))*p
                weight=summed_percepts1/len(self.percepts[n])

            else:
                weight=self.generalized_trust
            
            #loop through agents to get their trust values of self.partner
            for a in self.model.schedule.agent_buffer(shuffled=False):
                if a.unique_id in self.neighbors:
                    if self.partner.unique_id in a.percepts: 
                        k+=1
                        summed_percepts2=0.
                        for i, p in enumerate(a.percepts[self.partner.unique_id]):
                            summed_percepts2+=(1/(len(a.percepts[self.partner.unique_id])-i))*p
                        self.info+=summed_percepts2*weight
        if self.info != 0:
            self.info=self.info/k #averages info
            self.info=self.center(self.info)

    def check_wealth_update_trust(self):
        change=np.random.uniform() 
        #get last_trust_values
        if self.partner.unique_id in self.percepts:
            last_trust_value=self.percepts.get(self.partner.unique_id)
            #print("--id--",last_trust_value)
        else:
            last_trust_value=self.generalized_trust
            last_trust_value=list([float(last_trust_value)])

        trust_value=fsum(last_trust_value)/len(last_trust_value)        

        if self.last_wealth > self.wealth: 
            new_trust_value=trust_value-change*trust_value
            self.center(new_trust_value)
            last_trust_value.append(new_trust_value)
            self.percepts[self.partner.unique_id]=last_trust_value
            self.memory.append(0)
        
        else:
            new_trust_value=trust_value+change*trust_value
            self.center(new_trust_value)
            last_trust_value.append(new_trust_value)
            self.percepts[self.partner.unique_id]=last_trust_value
            self.memory.append(1)

    def center(self,x): #keep values between -1 and 1
        if x>=0:
            x=min(1,x)
        else:
            x=max(-1,x)
        return x
