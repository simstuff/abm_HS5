from model import TrustModel
import unittest


class ModelTest(unittest.TestCase):
    
    def test_init(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5)
        print(Model.G.nodes())
        self.assertEqual(len(Model.G.nodes()),4)

    def test_assign_trust_type(self):
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5)
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
        Model = TrustModel(num_nodes=4,increase=3,change_threshold=0.5)
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
            self.assertEqual(trustees[i],a.partner)

if __name__ == '__main__':
    unittest.main()