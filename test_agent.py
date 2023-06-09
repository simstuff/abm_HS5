import unittest
#from agent import agent
from model import TrustModel

class AgentTest(unittest.TestCase):

    def print_values_after_step():
        Model = TrustModel(4,3,0.5)
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
            print(i,a.type,a.wealth,a.generalized_trust,a.id)
        Model.step()
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
            print(i,a.type,a.wealth,a.generalized_trust,a.id)