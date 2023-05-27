import mesa
import numpy as np

class agent(mesa.Agent):
    def __init__(self, id):
        super().__init__(id)
        self.id = id
        self.generalized_trust=np.random.normal(loc=0.0,scale=1,size=None)
        self.personalized_trust=None #how to choose starting level?
        self.wealth=np.random.pareto(100) #pareto distribution for wealth
        self.type=None
        self.send_money=False
        self.suspectability=np.random.normal(loc=0.0,scale=1,size=None)
        self.percepts={"id":[],
                       "memory":{},#memory -> introduce forgetting? #best implemented as dict
                       "history":[0,0,0]} #percept history for change of generalized trust

    def step(self, partner):
        self.calculate_trust(partner)
        if self.wealth < 2*(1-self.personalized_trust):
            self.send_money=False
        else:
            self.send_money=True #send done in env
        
        change_prop=np.random.standard_normal()
        if change_prop > 0: #zufällige Wsl für Änderung von generalized trust
            self.change_of_generalized_trust(change_prop)

    #trust should be expressed as percentage to enable gradual sendings, send =1*trust, if < 0.5 no trust
    def calculate_trust(self,partner):
        for percept in self.percepts:
            if percept["id"]==partner.id:
                pass
            else:
                pass
        self.personalized_trust=(self.generalized_trust+self.personalized_trust)/2

    def change_of_generalized_trust(self,change_prop):
        for h in self.percepts["history"]:
            neg=0
            pos=0
            if h < 0:
                neg+=1
            else:
                pos+=1

        if pos > neg:
            self.generalized_trust=self.generalized_trust*change_prop #number of increase,how to choose?
    # choose agent
    # check money,
    # send money,
    # receive money, 
    # update trust value
