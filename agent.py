import mesa
import numpy as np

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
        self.last_partner=None
        self.neighbors=[] #to be initialized through grid
        self.memory=[]#sum all elements in array and if 3 then change generlaized trust
        self.security_level=np.random.uniform(low=1,high=1.5)

    def step(self):
        self.last_partner=self.partner
        if self.last_wealth is not None: #to not execute check in first round
            self.check_wealth_update_trust()
            self.memory
        self.interact()

    def interact(self):
        self.calculate_neighbor_info()
        trust_level=self.calculate_trust() #believe

        if self.type=="trustor":
            print("trustor acts")
            self.last_wealth=self.wealth
            if self.wealth > self.security_level*trust_level: #desire
                self.partner.wealth+=self.model.increase #intention
                print("increased wealth")
            
        else:
            print("trustee acts")
            if self.wealth > self.security_level*trust_level: #desire
                self.partner.wealth+=self.model.increase/2 #intention
                self.wealth-=self.model.increase/2
                print("decreased wealth")

        if len(self.memory) > 3:
            if sum(self.memory[-3:])==3:
                change_prop=np.random.uniform()
                if change_prop > self.model.change_threshold: #zufällige Wsl für Änderung von generalized trust
                    self.generalized_trust=self.generalized_trust+self.generalized_trust*change_prop
                    self.generalized_trust=self.center(self.generalized_trust)

                if sum(self.memory[-3:])==0:
                    change_prop=np.random.uniform(low=-1,high=0)
                    if change_prop < -1*self.model.change_threshold: #zufällige Wsl für Änderung von generalized trust
                        self.generalized_trust=self.generalized_trust+self.generalized_trust*change_prop
                        self.generalized_trust=self.center(self.generalized_trust)

       


    #trust should be expressed as percentage to enable gradual sendings, send =1*trust, if < 0.5 no trust
    def calculate_trust(self):
        if self.partner.unique_id in self.percepts:
            personalized_trust=self.percepts[self.partner.unique_id]
            trust_level=(((self.generalized_trust+personalized_trust)/2)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust+personalized_trust)/2

        else:
            if self.info==0:
                trust_level=self.generalized_trust
            else:
                trust_level=((self.generalized_trust)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust)
            self.percepts[self.partner.unique_id]=trust_level

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
                    if self.partner in a.percepts:
                        self.info+=a.percepts[self.partner.unique_id]*weight
        

        if self.info > 0:
            self.info=self.info/len(self.neighbors) #averages info

    def check_wealth_update_trust(self):
        if self.last_wealth > self.wealth:
            change=np.random.uniform() #make change distr responsive?
            if self.partner.unique_id in self.percepts:
                last_trust_value=self.percepts[self.partner.unique_id]
            else:
                last_trust_value=self.generalized_trust
            new_trust_value=last_trust_value-change*last_trust_value
            self.center(new_trust_value)
            self.percepts[self.partner.unique_id]=new_trust_value
            self.memory.append(0)
            print("Reduced trust")
        
        else:
            change=np.random.uniform()
            if self.partner.unique_id in self.percepts:
                last_trust_value=self.percepts[self.partner.unique_id]
            else:
                last_trust_value=self.generalized_trust            
            new_trust_value=last_trust_value+change*last_trust_value
            self.center(new_trust_value)
            self.percepts[self.partner.unique_id]=new_trust_value
            self.memory.append(1)
            print("Increased trust")

    def center(self,x): #keep values between -1 and 1
        if x>=0:
            x=min(1,x)
        else:
            x=max(-1,x)
        return x
