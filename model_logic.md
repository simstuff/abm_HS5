# Environment
- Agents are chosen randomly and are assigned trustor and trustee role randomly 
- The trustor can then send an endowment to trustee, which is trippled
-  The trustee can then send a certain amount back. 
- interaction is repeated to enable the formation of learning effects
- agents are embedded into a network to enable control mechanisms. The network is fixed and cannot be changed by agents. 
- The other agents in the network are also participating in a trust game in each round.
- After paring the agents and assigning them the role of trustee and trustor, the agents start playing a trust game. 
- The sequence in which the pairs are playing is chosen at random. From this follows that the number of agents needs to be even to allow for equal paring.
- agents are only influenced by their nearest neighbor. Two agents are nearest neighbors if the shortest path between them does not to go through a third agent. 
- agents are loosing a certain amount of their resources, which they are able to decrease through trusting as well as non trusting behavior by sending or returning an endowment or not sending or returning an endowment. 
- This “fee” will be taken from the agent at the end of every round. 
- If an agent is not able to pay this “fee” he “dies” and does not participate in the simulation anymore. 
- This means that a global performance measure for this model is the accumulated wealth of all agents and the average wealth of every agent as well as the number of agents “alive”.

# Agents
- have sensors with which they are able to perceive necessary information in their environment. 
- Whatever an agent perceives is called an percept and added to the percept sequence, which stores the complete history of an agent’s perceptions.
- In addition an agent needs an agent function, which describes the behavior of an agent for every possible input
## BDI-Model:
- The model incorporates three mental attitudes, believes, desires and intentions
- Believes represent the information the agent has about the world, which combines the percept sequence of the agent and any knowledge the agent is provided with at start of simulation.This means that, in the case of this paper, beliefs are the sum of an agent’s percept sequence and its social influence, calculated by formula (1)
- Desires are the states an agent would like to accomplish. In the case of this paper, this would comprise “survival” and high payoffs. These desires are, therefore, representing the agent’s goal. - An intention is a specific course of action, which the agent belives results in goal achievement. - Finally, the actual behavior is based on an agent’s actuators. These actuators are also called plans in the context of the BDI-model
-At each step of the simulation, the agents beliefs are updated in light of new information obtained in previous rounds and information from its nearest neighbors. The agent then selects its intention based in its belief. In this paper, this mean that, if an agent believes that the trustee she is interacting with is trustworthy, she will choose the intention to trust. After that the agents searches to the library of plans and chooses the actuator, in this case sending money, according to its beliefs and intentions. This step is also called the deliberation process (Balke and Gilbert 2014: 6). After these considerations, the actuators are quite simple to define. An agent can send money. This is the only behavior that represents trust in a trust game and that the agent is deliberately able to perform. From any other action, for example influencing other agents, is abstracted through the automatic influence of nearest neighbors in the influence network. Finally, an agent needs sensors in order to recognize trusting or not trusting behavior and social influence, to gather information and update its believes. Such sensors are implemented based on an agents wealth. If wealth has increased after sending money to an agent before the end of a round, the agent knows that its trustee behaved trustworthy. 
- In conclusion, an agent needs to have the following attributes: wealth (representing the amount of money an agent has), a susceptibility value, a set of percept sequences for every agent she interacts with, the ability to send money and the ability to recognize its nearest neighbors and perceive new information and update its beliefs according to the standard model of social influence network theory.

#Agents have a value to increase -> responsive