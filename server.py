import mesa
from model import TrustModel

trust_chart = mesa.visualization.ChartModule(
    [
        {"Label": "GeneralizedTrustingAgents", "Color": "#FF0000"},
        {"Label":"GeneralizedMistrustingAgents","Color":"#808081"},
    ]
)

avg_ptrust_chart=mesa.visualization.ChartModule(
    [
        {"Label":"AvgPersonalizedTrust","Color":"#808011"},
    ]
)

avg_gen_trust_chart=mesa.visualization.ChartModule(
    [
        {"Label":"AvgGeneralizedTrust","Color":"#808181"}
    ]
)

wealth_chart=mesa.visualization.ChartModule(
    [
        {"Label": "TotalWealth", "Color": "#FF0000"},
    ]
)

node_chart=mesa.visualization.ChartModule(
    [
        {"Label":"NumberOfNodes","Color":"#FF0000"},
    ]
)
def network_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(agent):
        if agent.generalized_trust<0:
            return "#FF0000"
        else:
            return "#008000"
      
    def edge_color(agent1, agent2):
        ptrust1=None
        ptrust2=None
        if agent2 in agent1.percepts:
            ptrust1=agent1.percepts[agent2]
        elif agent1 in agent2.percepts:
            ptrust2=agent2.percepts[agent1]
        else:
            return "#0810000"
        
        if ptrust1 is not None and ptrust2 is not None:
            ptrust=(ptrust1+ptrust2)/2
            if ptrust<0:
                return  "#FF0000"
            else:
                return  "#008000"

    def edge_width(agent1, agent2):
        if agent2.unique_id in agent1.percepts:
            sum_of_interactions1=agent1.percepts.get(agent2)
            if sum_of_interactions1 is not None:
                sum_of_interactions1=sum(sum_of_interactions1[-agent1.memory_span:])
        else:
            sum_of_interactions1=agent1.generalized_trust
        
        if sum_of_interactions1 is not None:
            if sum_of_interactions1<0:
                return sum_of_interactions1*-1
        else:
            return sum_of_interactions1

    def get_agents(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]
    

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": f"id: {agents[0].unique_id}<br>gTrust: {agents[0].generalized_trust}",
        }
        for (_, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": edge_color(*get_agents(source,target)),
            "width": edge_width(*get_agents(source,target))
        }
        #for (_, agents) in G.nodes.data("agent")
        for (source, target) in G.edges
    ]

    return portrayal

network=mesa.visualization.NetworkModule(portrayal_method=network_portrayal)


model_params={
    "num_nodes":mesa.visualization.Slider(name="num_nodes", value=50,min_value=10,max_value=100,step=2,description="number of nodes in network, must be even"),
    "increase":mesa.visualization.Slider(name="Wealth-Increase",value=3,min_value=1.5,max_value=10,step=0.5,description="amount by which welath is increased when agent trusts"),
    "change_threshold":mesa.visualization.Slider(name="Change_threshold",value=0.5,max_value=1,min_value=0.1,step=0.1,description="Probability to induce change of generalized trust"),
    "decrease":mesa.visualization.Slider(name="decrease",value=1,min_value=0,max_value=10, step=1,description="decrease of agents welath per model step"),
    "memory":mesa.visualization.Slider(name="memory",value=3,min_value=1,max_value=10,step=1,description="determines how many steps agent interactions are remembered by each agent,upper bound of uniform distribution"),
    "max_step":mesa.visualization.Slider(name="max_step",value=100,min_value=1,max_value=1000,step=1,description="end of simulation if steo = max_step"),

}
server = mesa.visualization.ModularServer(model_cls=TrustModel,visualization_elements=[wealth_chart,node_chart,trust_chart,avg_gen_trust_chart,avg_ptrust_chart],name="TrustModel",model_params=model_params ,port=8080)