from model import *
import unittest


class ModelTest(unittest.TestCase):
    
    def test_init(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0)
        print(Model.G.nodes())
        self.assertEqual(len(Model.G.nodes()),4)

    def test_assign_trust_type(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0)
        trustees = []
        trustors = []
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=True)):
            if i < Model.num_nodes/2:
                a.type="trustor"
                trustees.append(a)
            else:
                a.type="trustee"
                trustors.append(a)
        self.assertNotEqual(trustees,trustors)

    def test_assign_partners(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0)
        trustees = []
        trustors = []
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=True)):
            if i < Model.num_nodes/2:
                a.type="trustor"
                trustees.append(a)
            else:
                a.type="trustee"
                trustors.append(a)
        
        for i,a in enumerate(trustors):
            partner=trustees[i]
            a.partner=partner
            self.assertEqual(trustees[i],a.partner)#


    def test_get_avg_trust(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0)
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=True)):
            a.wealth=1
        tmp=total_wealth(Model)
        self.assertEqual(4,tmp)
        
    def test_personalized_trust_per_agent(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0)
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=True)):
            for b in Model.schedule.agent_buffer():
                a.percepts[b]=1
        tmp=personalized_trust_per_agent(Model)
        k=100
        t=0
        for key,val in tmp.items():
            self.assertNotEqual(key,k)
            key=k
            t+=val
        self.assertEqual(t,4)
            
            

    def test_personalized_trust_per_agent(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0)
        Model.step()
        tmp=personalized_trust_per_agent(Model)
        for val in tmp.values():
            for v in val.values():
                print(v)
                self.assertIsInstance(v,list)

if __name__ == '__main__':
    unittest.main()