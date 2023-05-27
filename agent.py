import mesa
import numpy as np

class agent(mesa.Agent):
    def __init__(self, id):
        super().__init__(id)
        self.id = id
        self.generalized_trust=np.random()
        self.personalized_trust=None #how to choose starting level?
        self.wealth=np.random()
        self.type=None
        self.send_money=False
        self.suspectability=np.random()
        self.percepts=[{"id":{}
                       "memory":},] #memory -> introduce forgetting? #best implemented as dict

    def step(self, partner):
        trust_level=0
        self.calculate_trust()
        if self.wealth < 2*(1-self.personalized_trust):
            self.send_money=False
        else:
            self.send_money=True #send done in env
        
        if np.random() > randomWert: #zufällige Wsl für Änderung von generalized trust
            self.change_of_generalized_trust

#trust should be expressed as percentage to enable gradual sendings, send =1*trust, if < 0.5 no trust
    def calculate_trust(self):
        for percept in self.percepts:
            if percept["id"]==partner.id:
                pass
            else:
                pass
        self.personalized_trust=(self.generalized_trust+self.personalized_trust)/2

    def change_of_generalized_trust(self):
        if n_interaction_positive > n_interaction_positive/interactions:
            self.generalized_trust=self.generalized_trust*1.2 #number of increase,how to choose?
    # choose agent
    # check money,
    # send money,
    # receive money, 
    # update trust value
