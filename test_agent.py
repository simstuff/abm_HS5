import unittest
from agent import TrustAgent
from model import TrustModel

class AgentTest(unittest.TestCase):

    def print_values_after_step():
        Model = TrustModel(4,3,0.5)
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
            print(i,a.type,a.wealth,a.generalized_trust,a.id)
        Model.step()
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
            print(i,a.type,a.wealth,a.generalized_trust,a.id)

    def test_center(self):
        Agent = TrustAgent(1,2)
        self.assertEqual(Agent.center(0),0)
        self.assertEqual(Agent.center(-2),-1)
        self.assertEqual(Agent.center(2),1)

    def test_check_wealth_update_trust(self):
        A=TrustAgent(1,2)
        B=TrustAgent(2,2)
        A.last_wealth=1
        A.wealth=0
        A.partner=B
        A.percepts[B]=1
        A.check_wealth_update_trust()
        self.assertLessEqual(A.percepts[B],1)
        self.assertEqual(A.memory[0],0)

        A.last_wealth=0
        A.wealth=1
        A.percepts[B]=0.5
        A.check_wealth_update_trust()
        self.assertGreaterEqual(A.percepts[B],0.5)
        self.assertEqual(A.memory[1],1)

    def test_calculate_neighbor_info(self):
        Model=TrustModel(10,3,0.5)
        for a in Model.schedule.agent_buffer(shuffled=False):
            a.calculate_neighbor_info()
            self.assertEqual(a.info,0)
        b=None
        for a in Model.schedule.agent_buffer(shuffled=False):
            a.percepts[b]=0.5
            b=a
        print("---",Model.grid.get_neighbors(node_id=1,include_center=False))
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
            a.calculate_neighbor_info()
            self.assertNotEqual(a.info,0)