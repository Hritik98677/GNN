import os
import json
import pickle

def find_capacitances(data):
    """
    Recursively find the 'Capacitances' key in a nested dictionary or list.
    Returns the list of capacitance entries if found, else None.
    """
    if isinstance(data, dict):
        for k, v in data.items():
            if k == "Capacitances":
                return v
            elif isinstance(v, (dict, list)):
                found = find_capacitances(v)
                if found is not None:
                    return found
    elif isinstance(data, list):
        for item in data:
            found = find_capacitances(item)
            if found is not None:
                return found
    return None

def update_graph_with_capacitances(gpr_dir, graphs_dir):
    for file in os.listdir(gpr_dir):
        if file.endswith(".gpr"):
            gpr_path = os.path.join(gpr_dir, file)
            pkl_file = file.replace(".gpr", ".pkl")
            pkl_path = os.path.join(graphs_dir, pkl_file)

            try:
                # Load .gpr data (json-like structure)
                with open(gpr_path, "r") as f:
                    gpr_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"JSON decode error in file {file}: {e}")
                print("Skipping this file.")
                print("---------------------------------------------------------------------------------------------")
                continue

            capacitances = find_capacitances(gpr_data)

            if capacitances is None:
                print(f"No 'Capacitances' found in {file}. Skipping.")
                print("---------------------------------------------------------------------------------------------")
                continue

            try:
                # Load corresponding graph pickle file
                with open(pkl_path, "rb") as f:
                    graph = pickle.load(f)
            except FileNotFoundError:
                print(f"Pickle file not found for {file}: {pkl_file}. Skipping.")
                print("---------------------------------------------------------------------------------------------")
                continue



            updated_edges = set()
            capacitance_edges = set()
            # Keep track of capacitance edges for quick lookup
            for cap in capacitances:
                capacitance_edges.add( (cap["SegmentGroup1"], cap["SegmentGroup2"]) )
                capacitance_edges.add( (cap["SegmentGroup2"], cap["SegmentGroup1"]) )

            # Insert capacitance values as edge attribute 'Value' where edge exists and is in capacitances
            for cap in capacitances:
                sg1 = cap["SegmentGroup1"]
                sg2 = cap["SegmentGroup2"]
                value = cap["Value"]

                # Check if edge exists in either direction and update 'Value'
                if (sg1, sg2) in graph.edges:
                    graph.edges[(sg1, sg2)]["Value"] = value
                    updated_edges.add((sg1, sg2))
                elif (sg2, sg1) in graph.edges:
                    graph.edges[(sg2, sg1)]["Value"] = value
                    updated_edges.add((sg2, sg1))

            # Find edges present but NOT updated (i.e., edge exists but no capacitance injected)
            edges_present = set(graph.edges.keys())
            edges_not_updated = edges_present - updated_edges

            # Remove edges from edges_not_updated if they appear in capacitance edges to focus on those not targeted
            edges_not_updated = {e for e in edges_not_updated if e not in capacitance_edges and (e[1], e[0]) not in capacitance_edges}

            # Save the updated graph back to file
            with open(pkl_path, "wb") as f:
                pickle.dump(graph, f)

            print(f"File: {pkl_file}")
            # print(f"Number of edges updated with capacitance values: {len(updated_edges)}")
            # print("Updated edges:")
            # for edge in updated_edges:
            #     print(f"  Edge {edge[0]} <-> {edge[1]}")

            # print(f"\nEdges present in graph but NOT updated with capacitance values: {len(edges_not_updated)}")
            # if edges_not_updated:
            #     print("Edges not updated:")
            #     for edge in edges_not_updated:
            #         print(f"  Edge {edge[0]} <-> {edge[1]}")
            if len(edges_not_updated)>0:
                print("Failed gts runs result")
            print("Total edges: ",len(updated_edges)+len(edges_not_updated))
            print("Edges updated: ",len(updated_edges))
            print("Edges not updated: ",len(edges_not_updated))
            print()
            print("---------------------------------------------------------------------------------------------")

# Example call (adjust your folder paths)
update_graph_with_capacitances("gpr", "graphs_gt")
