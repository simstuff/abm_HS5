import mesa
import numpy as np

class agent(mesa.Agent):
    def __init__(self, id:int):
        super().__init__(id)
        self.id=id
        self.generalized_trust=np.random.normal(loc=0.0,scale=1,size=None)
        self.wealth=np.random.pareto(10) #pareto distribution for wealth
        self.type=None
        self.send_money=False
        self.info=0 #sum of info from neighbors
        self.suspectability=np.random.uniform(low=0,high=1.0)
        self.percepts={}
        self.last_wealth=self.wealth
        self.last_partner=None
        self.neighbors=None #to be initialized through grid
        self.memory=[0,0,0]#sum all elements in array and if 3 then change generlaized trust
        #{"id":"personalizedTrust":0}
         #    -> introduce forgetting? #best implemented as dict
        

    def step(self, partner):
        self.check_wealth_update_trust()
        trust_level=self.calculate_trust(partner) #believe
        self.last_partner=partner.id
        if self.wealth < 2*trust_level: #desire
            self.send_money=False #intention
        else:
            self.send_money=True #send done in env
        
        if sum(self.memory)==3:
            change_prop=np.random.uniform()
            if change_prop > 0.5: #zufällige Wsl für Änderung von generalized trust
                self.change_of_generalized_trust(change_prop)
        if sum(self.memory)==0:
            change_prop=np.random.uniform(low=-1,high=0)
            if change_prop < -0.5: #zufällige Wsl für Änderung von generalized trust
                self.change_of_generalized_trust(change_prop)

    #trust should be expressed as percentage to enable gradual sendings, send =1*trust, if < 0.5 no trust
    def calculate_trust(self,partner):
        if partner.id in self.percepts:
            personalized_trust=self.percepts[partner.id].get("personalizedTrust")
            self.info=self.calculate_neighbor_info()
            trust_level=(((self.generalized_trust+personalized_trust)/2)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust+personalized_trust)/2

        else:
            self.info = self.calculate_neighbor_info()
            trust_level=((self.generalized_trust)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust+personalized_trust)/2
            self.percepts[partner.id]=trust_level

        return trust_level

    def calculate_neighbor_info(self):

        self.info=None #get neighbors and calculate following the equation
    
    def change_of_generalized_trust(self,change_prop):
        self.generalized_trust=self.generalized_trust+self.generalized_trust*change_prop

    def check_wealth_update_trust(self):
        if self.last_wealth < self.wealth:
            change=np.random.uniform()
            last_trust_value=self.percepts[self.last_partner]
            new_trust_value=last_trust_value-change*last_trust_value
            self.percepts[self.last_partner]=new_trust_value
        
        else:
            change=np.random.uniform()
            last_trust_value=self.percepts[self.last_partner]
            new_trust_value=last_trust_value+change*last_trust_value
            self.percepts[self.last_partner]=new_trust_value
