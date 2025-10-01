import os
import json
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import re
import glob

# Folder containing JSON files
input_folder = "/home/ubuntu/sivista_users/hritik/sivista_pro/data_injestion/json_files"

# Folder to save generated graphs
output_folder = "/home/ubuntu/sivista_users/hritik/sivista_pro/data_injestion/graphs"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to process a single JSON file and create graph
def process_json_and_create_graph(json_path, output_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    polygons = data["structures"][0]["elements"]

    # Extract M1 coordinates
    m1_coordinates=[]
    for poly in polygons:
        if (poly.get('layer_name') == 'M0' or poly.get('layer_name') == 'BSPowerRail') and poly.get('datatype')==0:
            m1_coordinates.append({"cordinates":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],"segment":poly["textPolygons"][0]})

    for i in m1_coordinates:
        for j in polygons:
            if j["id"]==i["segment"] and j["element"]=="text" and j["datatype"]==1:
                i["segment"]=j["text"] + "Metal1"

    grouped_data = defaultdict(list)
    for entry in m1_coordinates:
        grouped_data[entry['segment']].append(entry)

    m1_coordinates = []
    for segment, items in grouped_data.items():
        if len(items) >=1:
            items.sort(key=lambda y: y['cordinates'][3], reverse=True)
            for index, item in enumerate(items):
                item['segment'] = f"{item['segment']}Block{index + 1}"
        m1_coordinates.extend(items)


    # Extract M2 coordinates
    m2_coordinates=[]
    for poly in polygons:
        if poly.get('layer_name') == 'M1' and poly.get('datatype')==0:
            m2_coordinates.append({"cordinates":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],"segment":poly["textPolygons"][0]})

    for i in m2_coordinates:
        for j in polygons:
            if j["id"]==i["segment"] and j["element"]=="text" and j["datatype"]==1:
                i["segment"]=j["text"] + "Metal2"

    grouped_data = defaultdict(list)
    for entry in m2_coordinates:
        grouped_data[entry['segment']].append(entry)

    m2_coordinates = []
    for segment, items in grouped_data.items():
        if len(items) >=1:
            items.sort(key=lambda y: y['cordinates'][3], reverse=True)
            for index, item in enumerate(items):
                item['segment'] = f"{item['segment']}Block{index + 1}"
        m2_coordinates.extend(items)

    m1_m2_metals=m1_coordinates+m2_coordinates

    # Group by 'segment' (without blocks)
    grouped_data = defaultdict(list)
    for entry in m1_m2_metals:
        base_segment = entry['segment'].split('Metal')[0]
        grouped_data[base_segment].append(entry)

    ideal_conductor = []

    for segment, items in grouped_data.items():
        if len(items) > 1:
            max_item = max(items, key=lambda x: x['cordinates'][3])
            new_entry = {'cordinates': max_item['cordinates'], 'segment': segment.split('Metal')[0]}
            ideal_conductor.append(new_entry)
        else:
            new_entry = {'cordinates': items[0]['cordinates'], 'segment': items[0]['segment'].split('Metal')[0]}
            ideal_conductor.append(new_entry)

    # Extract vias between layers and process similarly (via_m1 and via_m2)
    via_m1_coordinates=[]
    for poly in polygons:
        if poly.get("isVia")==True and poly["datatype"]==0 and "M1" not in poly["layer_name"]:
            via_m1_coordinates.append({"cordinates":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],"segment":poly['adjacencyList']})

    for i in via_m1_coordinates:
        for j in polygons:
            if i['segment'][0]==j["id"] and len(j["textPolygons"])>0 and j["datatype"]==0:
                i["segment"]=j["textPolygons"][0]
                break
            elif i['segment'][1]==j["id"] and len(j["textPolygons"])>0 and j["datatype"]==0:
                i["segment"]=j["textPolygons"][0]
                break

    for i in via_m1_coordinates:
        for j in polygons:
            if j["id"]==i["segment"] and j["element"]=="text" and j["datatype"]==1:
                i["segment"]=j["text"] + "Metal1Via"

    grouped_data = defaultdict(list)
    for entry in via_m1_coordinates:
        grouped_data[entry['segment']].append(entry)

    for segment, items in grouped_data.items():
        if len(items)>1:
            items.sort(key=lambda x: (-x['cordinates'][3], x['cordinates'][0]))
            for index, item in enumerate(items):
                item['segment'] = f"{item['segment']}Block{index+1}"
        else:
            items[0]['segment'] = items[0]['segment']+"Block1"

    via_m1_coordinates = [item for sublist in grouped_data.values() for item in sublist]

    via_m2_coordinates=[]
    for poly in polygons:
        if poly.get("isVia")==True and poly["datatype"]==0 and "M1" in poly["layer_name"]:
            via_m2_coordinates.append({"cordinates":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],"segment":poly['adjacencyList']})

    for i in via_m2_coordinates:
        for j in polygons:
            if i['segment'][0]==j["id"] and len(j["textPolygons"])>0 and j["datatype"]==0:
                i["segment"]=j["textPolygons"][0]
                break
            elif i['segment'][1]==j["id"] and len(j["textPolygons"])>0 and j["datatype"]==0:
                i["segment"]=j["textPolygons"][0]
                break

    for i in via_m2_coordinates:
        for j in polygons:
            if j["id"]==i["segment"] and j["element"]=="text" and j["datatype"]==1:
                i["segment"]=j["text"] + "Metal2Via"

    grouped_data = defaultdict(list)
    for entry in via_m2_coordinates:
        grouped_data[entry['segment']].append(entry)

    for segment, items in grouped_data.items():
        if len(items)>1:
            items.sort(key=lambda x: (-x['cordinates'][3], x['cordinates'][0]))
            for index, item in enumerate(items):
                item['segment'] = f"{item['segment']}Block{index+1}"
        else:
            items[0]['segment'] = items[0]['segment']+"Block1"

    via_m2_coordinates = [item for sublist in grouped_data.values() for item in sublist]

    # Extract gate coordinates and process (NMOSGate and PMOSGate)
    gate_coordinates=[]
    for poly in polygons:
        if poly.get('layer_name') == 'NMOSGate' and poly.get("datatype")==0:

            if poly.get("planarConnectedPolygon") is not None:
                pmos_associated=poly["planarConnectedPolygon"]
                for p_poly in polygons:
                    if p_poly.get('id') == pmos_associated and p_poly.get('layer_name') == 'PMOSGate' and p_poly.get("datatype")==0 :
                        gate_coordinates.append({"cordinates_nmos":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],
                                               "cordinates_pmos":[p_poly["xy"][0][0],p_poly["xy"][0][1],p_poly["xy"][2][0],p_poly["xy"][2][1]],
                                               "segment":poly['adjacencyList']+p_poly['adjacencyList']})
                        break
            elif poly.get('layer_name') == 'NMOSGate' and poly.get("datatype")==0 and poly.get("planarConnectedPolygon") is None and len(poly['adjacencyList'])!=0:
                gate_coordinates.append({"cordinates_nmos":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],
                                               "segment":poly['adjacencyList']})


        elif poly.get('layer_name') == 'PMOSGate' and poly.get("datatype")==0 and poly.get("planarConnectedPolygon") is None and len(poly['adjacencyList'])!=0:
            gate_coordinates.append({"cordinates_pmos":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],
                                           "segment":poly['adjacencyList']})


    for i in gate_coordinates:
        for j in polygons:
            if i['segment'][0]==j["id"] and j["datatype"]==0:
                i["segment"]=j["adjacencyList"]
                break


    for i in gate_coordinates:
        for j in polygons:
            if i['segment'][0]==j["id"] and len(j["textPolygons"])>0 and j["datatype"]==0:
                i["segment"]=j["textPolygons"][0]
                break
            elif i['segment'][1]==j["id"] and len(j["textPolygons"])>0 and j["datatype"]==0:
                i["segment"]=j["textPolygons"][0]
                break


    for i in gate_coordinates:
        for j in polygons:
            if j["id"]==i["segment"] and j["element"]=="text" and j["datatype"]==1:
                i["segment"]=j["text"] + "GateLine"

    for item in gate_coordinates:
        if 'cordinates_nmos' in item and 'cordinates_pmos' in item:
            nmos = item['cordinates_nmos']
            pmos = item['cordinates_pmos']
            if nmos[1] < pmos[1]:
                item['cordinates'] = [nmos[0], nmos[1], pmos[2], pmos[3]]
                del item['cordinates_nmos']
                del item['cordinates_pmos']
            elif nmos[1] > pmos[1]:
                item['cordinates'] = [pmos[0], pmos[1], nmos[2], nmos[3]]
                del item['cordinates_nmos']
                del item['cordinates_pmos']

    groups = defaultdict(list)
    for item in gate_coordinates:
        coord_key = 'cordinates' if 'cordinates' in item else 'cordinates_nmos' if 'cordinates_nmos' in item else 'cordinates_pmos'
        coordinates = item[coord_key]
        segment = item['segment']
        groups[segment].append((coordinates, coord_key, item))

    renamed_gate_coordinates = []
    for segment, items in groups.items():
        if len(items)>=1:
            items.sort(key=lambda x: (-x[0][3], x[0][2]))
            for i, (coordinates, coord_key, original_item) in enumerate(items, start=1):
                new_segment_name = f"{segment}Block{i}"
                original_item['segment'] = new_segment_name
                renamed_gate_coordinates.append(original_item)
        else:
            renamed_gate_coordinates.append(items[0][2])

    gate_coordinates = renamed_gate_coordinates

    # Extract diffcon coordinates similarly (NMOSInterconnect, PMOSInterconnect)
    diffcon_coordinates=[]
    for poly in polygons:
        if poly.get('layer_name') == 'NMOSInterconnect' and poly.get("datatype")==0:

            if poly.get("planarConnectedPolygon") is not None:
                pmos_associated=poly["planarConnectedPolygon"]
                for p_poly in polygons:
                    if p_poly.get('id') == pmos_associated and p_poly.get('layer_name') == 'PMOSInterconnect' and p_poly.get("datatype")==0:
                        diffcon_coordinates.append({"cordinates_nmos":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],
                                               "cordinates_pmos":[p_poly["xy"][0][0],p_poly["xy"][0][1],p_poly["xy"][2][0],p_poly["xy"][2][1]],
                                               "segment":poly['adjacencyList']+p_poly['adjacencyList']})
                        break
            else:
                diffcon_coordinates.append({"cordinates_nmos":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],
                                               "segment":poly['adjacencyList']})
        elif poly.get('layer_name') == 'PMOSInterconnect' and poly.get("datatype")==0 and poly.get("planarConnectedPolygon") is None:
            diffcon_coordinates.append({"cordinates_pmos":[poly["xy"][0][0],poly["xy"][0][1],poly["xy"][2][0],poly["xy"][2][1]],
                                           "segment":poly['adjacencyList']})

    for i in diffcon_coordinates:
        for j in polygons:
            if len(i["segment"])>0:
                if i['segment'][0]==j["id"] and j["datatype"]==0:
                    i["segment"]=j["adjacencyList"]
                    break

    for i in diffcon_coordinates:
        for j in polygons:
            if len(i["segment"])>0:
                if i['segment'][0]==j["id"] and len(j["textPolygons"])>0 and j["datatype"]==0:
                    i["segment"]=j["textPolygons"][0]
                    break
                elif i['segment'][1]==j["id"] and len(j["textPolygons"])>0 and j["datatype"]==0:
                    i["segment"]=j["textPolygons"][0]
                    break

    for i in diffcon_coordinates:
        for j in polygons:
            if len(i["segment"])>0:
                if j["id"]==i["segment"] and j["element"]=="text" and j["datatype"]==1:
                    i["segment"]=j["text"] + "Diffcon"

    for item in diffcon_coordinates:
        if 'cordinates_nmos' in item and 'cordinates_pmos' in item:
            nmos = item['cordinates_nmos']
            pmos = item['cordinates_pmos']
            if nmos[1] < pmos[1]:
                item['cordinates'] = [nmos[0], nmos[1], pmos[2], pmos[3]]
                del item['cordinates_nmos']
                del item['cordinates_pmos']
            elif nmos[1] > pmos[1]:
                item['cordinates'] = [pmos[0], pmos[1], nmos[2], nmos[3]]
                del item['cordinates_nmos']
                del item['cordinates_pmos']

    candidates = []
    for i, item in enumerate(diffcon_coordinates):
        if isinstance(item.get("segment"), list) and item["segment"] == []:
            coords = item.get("cordinates") or item.get("cordinates_nmos") or item.get("cordinates_pmos")
            top_right_x = coords[2]
            top_right_y = coords[3]
            candidates.append((i, top_right_x, top_right_y))

    candidates.sort(key=lambda x: (-x[2], x[1]))

    for idx, (i, _, _) in enumerate(candidates, start=1):
        diffcon_coordinates[i]["segment"] = f"DiffconBlock{idx}"

    groups = defaultdict(list)
    for item in diffcon_coordinates:
        coord_key = 'cordinates' if 'cordinates' in item else 'cordinates_nmos' if 'cordinates_nmos' in item else 'cordinates_pmos'
        coordinates = item[coord_key]
        segment = item['segment']
        groups[segment].append((coordinates, coord_key, item))

    renamed_diffcon_coordinates = []
    for segment, items in groups.items():
        if len(items)>=1:
            items.sort(key=lambda x: (-x[0][3], x[0][2]))
            for i, (coordinates, coord_key, original_item) in enumerate(items, start=1):
                new_segment_name = f"{segment}Block{i}"
                original_item['segment'] = new_segment_name
                renamed_diffcon_coordinates.append(original_item)
        else:
            renamed_diffcon_coordinates.append(items[0][2])

    diffcon_coordinates = renamed_diffcon_coordinates

    for i in diffcon_coordinates:
        if i["segment"].count("Block")>1:
            i["segment"]=i["segment"][:-6]

    final_segment_cordinates=gate_coordinates+diffcon_coordinates+via_m1_coordinates+m1_coordinates+via_m2_coordinates+m2_coordinates+ideal_conductor
    for i in final_segment_cordinates:
        if i["segment"].count("Block")>1:
            i["segment"]=i["segment"][:-6]

    ideal_conductor_cords=ideal_conductor
    ideal_conductor=[]
    for poly in polygons:
        if poly.get('element') == 'text' and poly.get("datatype")==1:
            ideal_conductor.append(poly.get("text"))

    ideal_conductor=set(ideal_conductor)
    metal1=[]
    metal2=[]
    via_m1=[]
    via_m2=[]
    gate=[]
    diffcon=[]

    for pin in ideal_conductor:
        for segment in final_segment_cordinates:
            if segment["segment"].startswith(pin+"Metal1Block"):
                metal1.append(segment["segment"])

    for pin in ideal_conductor:
        for segment in final_segment_cordinates:
            if segment["segment"].startswith(pin+"Metal2Block"):
                metal2.append(segment["segment"])

    for pin in ideal_conductor:
        for segment in final_segment_cordinates:
            if segment["segment"].startswith(pin+"Metal1Block"):
                metal1.append(segment["segment"])

    for pin in ideal_conductor:
        for segment in final_segment_cordinates:
            if segment["segment"].startswith(pin+"Metal1ViaBlock"):
                via_m1.append(segment["segment"])

    for pin in ideal_conductor:
        for segment in final_segment_cordinates:
            if segment["segment"].startswith(pin+"Metal2ViaBlock"):
                via_m2.append(segment["segment"])

    for pin in ideal_conductor:
        for segment in final_segment_cordinates:
            if segment["segment"].startswith(pin+"GateLineBlock"):
                gate.append(segment["segment"])

    for pin in ideal_conductor:
        for segment in final_segment_cordinates:
            if segment["segment"].startswith(pin+"DiffconBlock") or segment["segment"].startswith("Diffcon"):
                diffcon.append(segment["segment"])
    diffcon=set(diffcon)
    diffcon=list(diffcon)

    # No edge detection between metal1/metal2 and ideal conductor
    no_edge=[]
    for i in ideal_conductor_cords:
        for j in m1_m2_metals:
            if i["cordinates"]==j["cordinates"]:
                no_edge.append(f"{i['segment']}-->{j['segment']}")
                break

    # No edge between diffcons
    for i in range(0,len(diffcon)-1):
        for j in range(i+1,len(diffcon)):
            no_edge.append(f"{diffcon[i]}-->{diffcon[j]}")

    # Intersection area calculation function
    def intersection_area(rect1, rect2):
        x1_min, y1_min, x1_max, y1_max = rect1
        x2_min, y2_min, x2_max, y2_max = rect2
        overlap_width = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
        overlap_height = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))
        return overlap_width * overlap_height

    # Edge analysis of M1 metal and via_m1
    matches = []
    for via in via_m1_coordinates:
        best_segment = None
        best_area = 0
        for metal in m1_coordinates:
            area = intersection_area(via['cordinates'], metal['cordinates'])
            if area > best_area:
                best_area = area
                best_segment = metal['segment']
        matches.append({
            'via_segment': via['segment'],
            'matched_metal1_segment': best_segment,
            'overlap_area': best_area
        })

    for match in matches:
        no_edge.append(f"{match['via_segment']}-->{match['matched_metal1_segment']}")

    # Edge analysis of M2 metal and via_m2
    matches = []
    for via in via_m2_coordinates:
        best_segment = None
        best_area = 0
        for metal in m2_coordinates:
            area = intersection_area(via['cordinates'], metal['cordinates'])
            if area > best_area:
                best_area = area
                best_segment = metal['segment']
        matches.append({
            'via_segment': via['segment'],
            'matched_metal1_segment': best_segment,
            'overlap_area': best_area
        })

    for match in matches:
        no_edge.append(f"{match['via_segment']}-->{match['matched_metal1_segment']}")

    # Edge analysis of M1 metal and via_m2
    matches = []
    for via in via_m2_coordinates:
        best_segment = None
        best_area = 0
        for metal in m1_coordinates:
            area = intersection_area(via['cordinates'], metal['cordinates'])
            if area > best_area:
                best_area = area
                best_segment = metal['segment']
        matches.append({
            'via_segment': via['segment'],
            'matched_metal1_segment': best_segment,
            'overlap_area': best_area
        })

    for match in matches:
        no_edge.append(f"{match['via_segment']}-->{match['matched_metal1_segment']}")

    # Helper to extract coordinates regardless of key name
    def get_coords(item):
        for key in ('cordinates', 'cordinates_pmos', 'cordinates_nmos'):
            if key in item:
                return item[key]
        raise KeyError(f"No coordinate key found in {item}")

    # Edge analysis of via_m1 and gate
    matches = []
    via_segments_to_remove = []

    for via in via_m1_coordinates:
        via_coords = get_coords(via)
        best_segment = None
        best_area = 0
        for gate in gate_coordinates+diffcon_coordinates:
            gate_coords = get_coords(gate)
            area = intersection_area(via_coords, gate_coords)
            if area > best_area:
                best_area = area
                best_segment = gate['segment']
        matches.append({
            'via_segment': via['segment'],
            'matched_gate_segment': best_segment,
            'overlap_area': best_area
        })
        if best_area > 0:
            no_edge.append(f"{via['segment']}-->{best_segment}")
            via_segments_to_remove.append(via['segment'])

    # Remove via segments overlapping gates
    via_m1_coordinates = [via for via in via_m1_coordinates if via['segment'] not in via_segments_to_remove]

   

    # Prepare graph edges excluding no_edge relations
    exclude_edges=no_edge
    list2= final_segment_cordinates

    exclude_set = set()
    for edge in exclude_edges:
        edge = edge.replace("→", "-->")
        src, dst = edge.replace(" ", "").split("-->")
        exclude_set.add((src, dst))
        exclude_set.add((dst, src))

    # Create graph
    G = nx.Graph()

    # Add nodes with their coordinates as attributes
    for seg_info in list2:
        segment_name = seg_info['segment']
        # Use whichever coordinates exist (nmos or pmos)
        coordinates = seg_info.get('cordinates_nmos') or seg_info.get('cordinates_pmos') or seg_info.get('cordinates')
        G.add_node(segment_name, coordinates=coordinates)

    # Add edges (complete graph minus excluded edges)
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            n1, n2 = nodes[i], nodes[j]
            if (n1, n2) not in exclude_set:
                G.add_edge(n1, n2)

    # Rename nodes removing special characters
    mapping = {}
    for node in G.nodes():
        new_name = re.sub(r"[^a-zA-Z0-9]", "", node)
        if new_name != node:
            mapping[node] = new_name

    G = nx.relabel_nodes(G, mapping)

    # Save graph as pickle
    with open(output_path, "wb") as f:
        pickle.dump(G, f)

    # Plot and save graph
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G, pos, with_labels=True,
        node_color="skyblue", node_size=1800,
        font_size=8, edge_color="gray"
    )
    plt.title(f"Graph: {G.number_of_nodes()} Nodes, {G.number_of_edges()} Edges")
    plt.savefig(output_path.replace('.pkl', '.png'), dpi=300)
    plt.close()
    
    print(f"✅ Graph created for {json_path}")
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print("------------------------------------------------------------------------------------------")

# Loop through all JSON files and process each
json_files = glob.glob(os.path.join(input_folder, "*.json"))
for json_file in json_files:
    file_name = os.path.basename(json_file)
    graph_file = os.path.join(output_folder, file_name.replace('.json', '.pkl'))
    process_json_and_create_graph(json_file, graph_file)
   

print(f"✅ All graphs created and saved in {output_folder}")
