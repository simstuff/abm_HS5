import unittest
from server import *
from agent import *
from model import *

class ServerTest(unittest.TestCase):

    def test_node_color(self):
        Model=TrustModel(1,0.5,0.5,0.5,1)
        color="#008000"
        for a in Model.schedule.agent_buffer(shuffled=True):
            a.generalized_trust=0.5
       
        portrayal=network_portrayal(Model.G)
        cc=portrayal["nodes"][0]["color"]
        self.assertEqual(color,cc)

    def test_edge_color(self):
        Model=TrustModel(2,0.5,0.5,0.5,1)
        color="#008000"
        b=None
        Model.step()
        for a in Model.schedule.agent_buffer(shuffled=False):
            if b is not None:
                a.percepts[b]=1
            b=a
        portrayal=network_portrayal(Model.G)
        print(portrayal)
        #self.assertEqual(portrayal["edges"][0]["color"],"#0810000")
