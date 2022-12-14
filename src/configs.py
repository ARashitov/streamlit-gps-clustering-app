import json
import logging

heading = """
# 🚛 GPS records clustering system

👣 User guide:
1. Choose `csv` of GPS files
2. Upload
3. Observe results

🚫 Constraints
1. Only one unique vehicle in a file
2. No any GPS timestamp duplicates
"""

MAP_HEIGHT = 700


kepler_map_config = None
try:
    with open('config/kepler_map_configuration.json') as f:
        kepler_map_config = json.load(f)
except Exception as exc:
    logging.error(f"Fail to read map config: {exc}")
