from model import TrustModel

Model = TrustModel(4,3,0.5)
for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
    print(i,a.type,a.wealth,a.generalized_trust,a.id)
Model.step()
for i,a in enumerate(Model.schedule.agent_buffer(shuffled=False)):
    print(i,a.type,a.wealth,a.generalized_trust,a.id)