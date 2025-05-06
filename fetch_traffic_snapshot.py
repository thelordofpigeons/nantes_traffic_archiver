import requests
import pandas as pd
from datetime import datetime, timezone
import os
import traceback

ARCHIVE_DIR = "archive"
LOG_FILE = "log_output.txt"

def log(message):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def fetch_realtime_traffic_snapshot(limit=100):
    dataset_id = "244400404_fluidite-axes-routiers-nantes-metropole"
    base_url = f"https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/{dataset_id}/records"
    offset = 0
    all_data = []

    while True:
        params = {
            "limit": limit,
            "offset": offset,
            "order_by": "mf1_hd"
        }

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")

        results = response.json().get("results", [])
        if not results:
            break

        all_data.extend(results)
        if len(results) < limit:
            break
        offset += limit

    return pd.DataFrame(all_data)

def save_snapshot_to_csv(df):
    if df.empty:
        log("⚠️ No data to save.")
        return

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{ARCHIVE_DIR}/nantes_traffic_snapshot_{timestamp}.csv"
    df.to_csv(filename, index=False)
    log(f"✅ Snapshot saved to '{filename}'")

if __name__ == "__main__":
    try:
        log("🚀 Starting traffic data fetch...")
        df = fetch_realtime_traffic_snapshot()
        save_snapshot_to_csv(df)
        log("✅ Script finished successfully.\n")
    except Exception as e:
        log("❌ An error occurred:")
        log(traceback.format_exc())
