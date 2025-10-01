import json
import os

# Custom JSON encoder to force single-line lists for textPolygons
class CustomEncoder(json.JSONEncoder):
    def iterencode(self, o, _one_shot=False):
        for chunk in super().iterencode(o, _one_shot=_one_shot):
            yield chunk

    def encode(self, o):
        if isinstance(o, dict) and "textPolygons" in o:
            tp = o["textPolygons"]
            if isinstance(tp, list) and len(tp) <= 4:  # small list -> one line
                # Format manually
                tp_str = "[ " + ", ".join(json.dumps(x) for x in tp) + " ]"
                new_obj = {**o, "textPolygons": None}
                s = super().encode(new_obj)
                # Replace placeholder with custom formatting
                return s.replace('"textPolygons": null', f'"textPolygons": {tp_str}')
        return super().encode(o)


def update_json_file(file_path, output_folder):
    # Skip FSP files
    if "FSP" in os.path.basename(file_path):
        print(f"Skipping FSP file: {file_path}")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    updated = False

    for structure in data.get("structures", []):
        elements = structure.get("elements", [])

        # Collect text elements (VSS/VDD with IDs)
        text_map = {}
        for el in elements:
            if el.get("element") == "text":
                txt = el.get("text", "")
                if txt in ["VSS", "VDD"]:
                    text_map[txt] = el.get("id")

        if "VSS" not in text_map or "VDD" not in text_map:
            continue  # No power rails in this structure

        vss_id = text_map["VSS"]
        vdd_id = text_map["VDD"]

        # Find BSPowerRail polygons with datatype=0
        bsp_polygons = [
            el for el in elements
            if el.get("element") == "boundary"
            and el.get("datatype") == 0
            and el.get("layer_name") == "BSPowerRail"
            and isinstance(el.get("textPolygons"), list)
        ]

        if len(bsp_polygons) >= 2:
            # Overwrite textPolygons (clean, no appending)
            bsp_polygons[0]["textPolygons"] = [vss_id]
            bsp_polygons[1]["textPolygons"] = [vdd_id]
            updated = True

    # Cleanup: remove "_dup" if any
    for structure in data.get("structures", []):
        for el in structure.get("elements", []):
            if "textPolygons" in el and isinstance(el["textPolygons"], list):
                el["textPolygons"] = [tp.replace("_dup", "") for tp in el["textPolygons"]]

    if updated:
        # Save updated file into the output folder
        base_name = os.path.basename(file_path)
        out_path = os.path.join(output_folder, base_name.replace(".json", "_updated.json"))
        with open(out_path, "w") as f:
            json.dump(
                data,
                f,
                indent=2,
                separators=(", ", ": "),
                cls=CustomEncoder
            )
        print(f"Updated file saved as {out_path}")
    else:
        print(f"No updates needed for {file_path}")


def process_folder(input_folder, output_folder=None):
    if output_folder is None:
        output_folder = input_folder  # save in same folder if no output specified

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)
            update_json_file(file_path, output_folder)


# === Example usage ===
input_folder = r"/home/ayush/gpr_analysis/json_folder"   # <-- change this path
output_folder = r"/home/ayush/gpr_analysis/json_folder"  # updated files here
process_folder(input_folder, output_folder)
