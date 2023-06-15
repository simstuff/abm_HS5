import mesa
from model import TrustModel

trust_chart = mesa.visualization.ChartModule(
    [
        {"Label": "PersonalizedTrust", "Color": "#008000"},
        {"Label": "GeneralizedTrustingAgents", "Color": "#808080"},
        {"Label":"GeneralizedMistrustingAgents","Color":"#808081"},
        {"Label":"AvgPersonalizedTrust","Color":"#808011"},
    ],
)

avg_gen_trust_chart=mesa.visualization.ChartModule(
    [
        {"Label":"AvgGeneralizedTrust","Color":"#808181"}
    ]
)

wealth_chart=mesa.visualization.ChartModule(
    [
        {"Label": "Wealth", "Color": "#FF0000"},
    ]
)

model_params={
    "num_nodes":mesa.visualization.Slider(name="num_nodes", value=50,min_value=10,max_value=100,step=2,description="number of nodes in network, must be even"),
    "increase":mesa.visualization.Slider(name="Wealth-Increase",value=3,min_value=1.5,max_value=10,step=0.5,description="amount by which welath is increased when agent trusts"),
    "change_threshold":mesa.visualization.Slider(name="Change_threshold",value=0.5,max_value=1,min_value=0.1,step=0.1,description="Probability to induce change of generalized trust"),
    "decrease":mesa.visualization.Slider(name="decrease",value=1,min_value=0,max_value=10, step=1,description="decrease of agents welath per model step")
}
server = mesa.visualization.ModularServer(model_cls=TrustModel,visualization_elements=[wealth_chart,trust_chart,avg_gen_trust_chart],name="MyModel",model_params=model_params ,port=8080)