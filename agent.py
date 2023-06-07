import mesa
import numpy as np
import model

class agent(mesa.Agent):
    def __init__(self, id:int,model):
        super().__init__(id)
        self.id=id
        self.generalized_trust=np.random.normal(loc=0.0,scale=1,size=None)
        self.wealth=np.random.pareto(10) #pareto distribution for wealth
        self.type=None
        self.send_money=False
        self.info=[] #sum of info from neighbors
        self.suspectability=np.random.uniform(low=0,high=1.0)
        self.percepts={}
        self.last_wealth=self.wealth
        self.model=model
        self.partner=None
        self.last_partner_id=None
        self.neighbors=[] #to be initialized through grid
        self.memory=[0,0,0]#sum all elements in array and if 3 then change generlaized trust
        #{"id":"personalizedTrust":0}
         #    -> introduce forgetting? #best implemented as dict
        

    def step(self, partner):
        self.last_partner_id=partner.id
        self.check_wealth_update_trust()
        trust_level=self.calculate_trust(partner) #believe
        if self.wealth < 2*trust_level: #desire
            self.send_money=False #intention
        else:
            self.send_money=True #send done in env
        
        if sum(self.memory)==3:
            change_prop=np.random.uniform()
            if change_prop > 0.5: #zufällige Wsl für Änderung von generalized trust
                self.generalized_trust=self.generalized_trust+self.generalized_trust*change_prop
        if sum(self.memory)==0:
            change_prop=np.random.uniform(low=-1,high=0)
            if change_prop < -0.5: #zufällige Wsl für Änderung von generalized trust
                self.generalized_trust=self.generalized_trust+self.generalized_trust*change_prop

    #trust should be expressed as percentage to enable gradual sendings, send =1*trust, if < 0.5 no trust
    def calculate_trust(self):
        if self.last_partner_id in self.percepts:
            personalized_trust=self.percepts[self.last_partner_id].get("personalizedTrust")
            self.info=self.calculate_neighbor_info()
            trust_level=(((self.generalized_trust+personalized_trust)/2)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust+personalized_trust)/2

        else:
            self.info = self.calculate_neighbor_info()
            if self.info==0:
                trust_level=self.generalized_trust
            else:
                trust_level=((self.generalized_trust)*(1-self.suspectability))+self.suspectability*self.info*(self.generalized_trust+personalized_trust)/2
            self.percepts[self.last_partner_id]=trust_level

        return trust_level

    def calculate_neighbor_info(self):
        self.info=0
        self.neighbors=self.model.network.get_neighbors(node_id=self.id, include_center=False, radius=1)

        for n in self.neighbors:
            if n.id in self.percepts:
                weight=self.percepts[n.id]
                if self.last_partner_id in n.percepts:
                    self.info+=n.percepts[self.last_partner_id]*weight

        if self.info > 0:
            self.info=self.info/len(self.neighbors)

    def check_wealth_update_trust(self):
        if self.last_wealth < self.wealth:
            change=np.random.uniform()
            last_trust_value=self.percepts[self.last_partner_id]
            new_trust_value=last_trust_value-change*last_trust_value
            self.percepts[self.last_partner_id]=new_trust_value
        
        else:
            change=np.random.uniform()
            last_trust_value=self.percepts[self.last_partner_id]
            new_trust_value=last_trust_value+change*last_trust_value
            self.percepts[self.last_partner_id]=new_trust_value
