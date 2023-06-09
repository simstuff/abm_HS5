import mesa
import agent
import model
import matplotlib as plt
import pandas as pd
# use optuna to find ideal model config, e.g model that maximizes trust? maybe + steps taken to get there?
seed=42
total_trust = []
trust_dst = "poisson"
# This runs the model 100 times, each model executing 10 steps.
for j in range(100):
    # Run the model
    model = model(10)
    for i in range(10):
        model.step()
        # Store the results
    for agent in model.schedule.agents:
        total_trust.append(agent.wealth)
    plt.hist(total_trust, bins=range(max(total_trust) + 1))

    data = model.datacollector.get_model_vars_dataframe()
    data.to_csv("/path")
