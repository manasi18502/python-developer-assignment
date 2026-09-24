import json
import math
import sys
import os

def distance(point1, point2):
    return math.sqrt(
        (point1[0] - point2[0]) ** 2
        + (point1[1] - point2[1]) ** 2
    )


if len(sys.argv) > 1:
    input_file = sys.argv[1]

elif os.path.exists("base_case.json"):
    input_file = "base_case.json"

elif os.path.exists("data.json"):
    input_file = "data.json"

else:
    input_file = "test_case_1.json"


with open(input_file, "r") as file:
    data = json.load(file)



 

if isinstance(data["warehouses"], dict):

    warehouses = data["warehouses"]
    agents = data["agents"]

else:

    # Format 2:
    # "warehouses": [
    #     {"id": "W1", "location": [0, 0]}
    # ]

    warehouses = {
        warehouse["id"]: warehouse["location"]
        for warehouse in data["warehouses"]
    }

    agents = {
        agent["id"]: agent["location"]
        for agent in data["agents"]
    }


 
assignments = []


 
for package in data["packages"]:

    package_id = package["id"]

    # Support both:
    # "warehouse": "W1"
    # and
    # "warehouse_id": "W1"

    if "warehouse" in package:
        warehouse_id = package["warehouse"]
    else:
        warehouse_id = package["warehouse_id"]

    destination = package["destination"]

    warehouse_location = warehouses[warehouse_id]


    # Find nearest agent
    nearest_agent = None
    shortest_distance = float("inf")

    for agent_id, agent_location in agents.items():

        agent_to_warehouse = distance(
            agent_location,
            warehouse_location
        )

        if agent_to_warehouse < shortest_distance:
            shortest_distance = agent_to_warehouse
            nearest_agent = agent_id


    # Warehouse to destination
    warehouse_to_destination = distance(
        warehouse_location,
        destination
    )


    # Total delivery distance
    total_distance = (
        shortest_distance
        + warehouse_to_destination
    )


    assignments.append({
        "package_id": package_id,
        "agent_id": nearest_agent,
        "warehouse_id": warehouse_id,
        "destination": destination,
        "total_distance": total_distance
    })


 
print("FINAL PACKAGE ASSIGNMENTS")
print("-------------------------")

for assignment in assignments:

    print(
        assignment["package_id"],
        "->",
        assignment["agent_id"],
        "->",
        assignment["warehouse_id"],
        "->",
        assignment["destination"]
    )

    print(
        "Total Distance:",
        round(assignment["total_distance"], 2)
    )


# -------------------------------------------------
# Create agent report
# -------------------------------------------------

agent_report = {}

for agent_id in agents:

    agent_report[agent_id] = {
        "packages_delivered": 0,
        "total_distance": 0.0
    }


 
for assignment in assignments:

    agent_id = assignment["agent_id"]

    agent_report[agent_id]["packages_delivered"] += 1

    agent_report[agent_id]["total_distance"] += (
        assignment["total_distance"]
    )


 
for agent_id in agent_report:

    packages_delivered = (
        agent_report[agent_id]["packages_delivered"]
    )

    total_distance = (
        agent_report[agent_id]["total_distance"]
    )

    if packages_delivered > 0:

        efficiency = (
            total_distance / packages_delivered
        )

    else:

        efficiency = 0


    agent_report[agent_id]["total_distance"] = round(
        total_distance,
        2
    )

    agent_report[agent_id]["efficiency"] = round(
        efficiency,
        2
    )


 
best_agent = None
best_efficiency = float("inf")

for agent_id, details in agent_report.items():

    if details["packages_delivered"] > 0:

        efficiency = details["efficiency"]

        if efficiency < best_efficiency:

            best_efficiency = efficiency
            best_agent = agent_id


# Add best agent to report
agent_report["best_agent"] = best_agent


 
print()
print("AGENT REPORT")
print("------------")

for agent_id, details in agent_report.items():

    if agent_id != "best_agent":

        print(agent_id)

        print(
            "Packages Delivered:",
            details["packages_delivered"]
        )

        print(
            "Total Distance:",
            details["total_distance"]
        )

        print(
            "Efficiency:",
            details["efficiency"]
        )

        print()


print("Best Agent:", best_agent)


with open("report.json", "w") as file:

    json.dump(
        agent_report,
        file,
        indent=4
    )


print()
print("Report saved successfully to report.json")
