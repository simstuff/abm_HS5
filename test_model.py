from model import *
import unittest


class ModelTest(unittest.TestCase):
    
    def test_init(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0,memory=4)
        print(Model.G.nodes())
        self.assertEqual(len(Model.G.nodes()),4)

    def test_assign_trust_type(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0,memory=4)
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
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0,memory=4)
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
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0,memory=4)
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=True)):
            a.wealth=1
        tmp=total_wealth(Model)
        self.assertEqual(4,tmp)
        
    def test_personalized_trust_per_agent(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0,memory=4)
        count=0
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=True)):
            for b in Model.schedule.agent_buffer():
                a.percepts[b]=1
                count+=1
        tmp=personalized_trust_per_agent(Model)
        k=100
        t=0
        for key,val in tmp.items():
            self.assertNotEqual(key,k)
            key=k
            for v in val.values():
                t+=v
        self.assertEqual(t,count)
            
            

    def test_percepts_are_lists(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0,memory=4)
        Model.step()
        tmp=personalized_trust_per_agent(Model)
        for val in tmp.values():
            for v in val.values():
                self.assertIsInstance(v,list)

    def test_avg_ptrust(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5,decrease=0,memory=4)
        b=None
        for i,a in enumerate(Model.schedule.agent_buffer(shuffled=True)):
            if b is not None:
                a.percepts[b]=[1.0,1.0,1.5,1]
            b=a
        total=4.5
        avg_ptrust=get_avg_ptrust(Model)
        self.assertEqual(total,avg_ptrust)

if __name__ == '__main__':
    unittest.main()