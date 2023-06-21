import unittest
from agent import TrustAgent
from model import TrustModel

class AgentTest(unittest.TestCase):

    def print_values_after_step():
        Model = TrustModel(4,3,0.5,1)
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
            print(i,a.type,a.wealth,a.generalized_trust,a.id)
        Model.step()
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
            print(i,a.type,a.wealth,a.generalized_trust,a.id)

    def test_init(self):
        Model = TrustModel(4,3,0.5,1)
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
            self.assertEqual(a.unique_id,i)


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
        test=False
        Model=TrustModel(10,3,0.5,1)
        for a in Model.schedule.agent_buffer(shuffled=False):
            a.calculate_neighbor_info()
            self.assertEqual(a.info,0)
        b=None
        for a in Model.schedule.agent_buffer(shuffled=False):
            a.percepts[b]=0.5
            b=a
        for a in Model.schedule.agent_buffer(shuffled=False):

            a.calculate_neighbor_info()
            if a.info>=0:
                test=True
            self.assertTrue(test)
            test=False

    def test_calculate_trust(self):
        A=TrustAgent(1,3)
        B=TrustAgent(2,3)

        A.partner=B
        t_l=A.calculate_trust()
        self.assertEqual(t_l,A.generalized_trust)
        A.info=1.0
        t_l=A.calculate_trust()
        self.assertEqual(A.percepts[A.partner.unique_id],t_l)

    def test_dicts(self):
        A=TrustAgent(1,3)
        B=TrustAgent(2,3)

        A.partner=B

        tmp=B.unique_id
        t_l=A.calculate_trust()
        self.assertEqual(t_l,A.generalized_trust)
        A.info=1.0
        t_l=A.calculate_trust()
        self.assertEqual(A.percepts[A.partner.unique_id],t_l)
        self.assertEqual(tmp,A.partner.unique_id)
        self.assertTrue(tmp in A.percepts)
        for name, age in A.percepts.items():
            if age == A.percepts[B.unique_id]:
                tmp2=name
        self.assertEqual(tmp2,tmp)
