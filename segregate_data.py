import os
from datetime import datetime
import json
import pandas as pd
from pprint import pprint
from tqdm.auto import tqdm

states = os.listdir("./states")
output_dir = "./data/"

for state in states:
    rows_2023_24 = []
    rows_2024_25 = []
    districts = os.listdir(f"./states/{state}")
    for district in districts:
        if district == "getDistricts.json":
            continue

        # print(f"District : {district}")
        json_path = f"./states/{state}/{district}/features.json"
        if not os.path.exists(json_path):
            continue

        try:
            feature_info = json.load(open(json_path))

        except json.JSONDecodeError:
            print(f"Error reading {json_path}")
            continue

        for feature in feature_info:
            if feature["period"] in ["2023-24", "2024-25"]:

                if "date" not in feature["properties"].keys():
                    continue

                # dt = feature["properties"]["date"]
                # dt = datetime.strptime(dt, "%m/%d/%y, %I:%M %p")
                # year = dt.year

                # district, village, date, lat, long, [N, P, K, B, Fe, Zn, Cu, S, OC, pH, Mn, EC]
                try:
                    row = {
                        "district": district,
                        "village": feature["properties"].get("village", ""),
                        "date": feature["properties"].get("date", ""),
                        "lat": feature["latitude"],
                        "long": feature["longitude"],
                        "N": feature["properties"].get("N", ""),
                        "P": feature["properties"].get("P", ""),
                        "K": feature["properties"].get("K", ""),
                        "B": feature["properties"].get("B", ""),
                        "Fe": feature["properties"].get("Fe", ""),
                        "Zn": feature["properties"].get("Zn", ""),
                        "Cu": feature["properties"].get("Cu", ""),
                        "S": feature["properties"].get("S", ""),
                        "OC": feature["properties"].get("OC", ""),
                        "pH": feature["properties"].get("pH", ""),
                        "Mn": feature["properties"].get("Mn", ""),
                        "EC": feature["properties"].get("EC", ""),
                    }
                except KeyError:
                    pprint(feature["properties"])

                if feature["period"] == "2023-24":
                    rows_2023_24.append(row)
                else:
                    rows_2024_25.append(row)

    df1 = pd.DataFrame(rows_2023_24)
    df2 = pd.DataFrame(rows_2024_25)

    df1.to_csv(
        os.path.join(os.path.join(output_dir, "2023-24"), f"{state}_2023_24.csv"),
        index=False,
        encoding="utf-8",
    )
    print(f"Saved {state}_2023_24.csv with {len(df1)} records")
    df2.to_csv(
        os.path.join(os.path.join(output_dir, "2024-25"), f"{state}_2024_25.csv"),
        index=False,
        encoding="utf-8",
    )
    print(f"Saved {state}_2024_25.csv with {len(df2)} records")

print("All states completed")
