import requests
import json
from datetime import datetime

with open("sites.json") as f:
    sites = json.load(f)

results = []

for site in sites:

    try:
        response = requests.get(site, timeout=10)

        if response.status_code == 200:
            status = "UP"
        else:
            status = f"ERROR {response.status_code}"

    except:
        status = "DOWN"

    result = {
        "site": site,
        "status": status,
        "time": str(datetime.now())
    }

    print(result)

    results.append(result)

with open("history.json", "w") as f:
    json.dump(results, f, indent=2)
