from datetime import datetime
import os
import time

from pdb_utils import fetch_released_pdb_ids, save_to_csv
from metadata import fetch_metadata

def main():
    since_date = input("Enter a release date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(since_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    output_dir = f"uniprot_entries_{since_date.replace('-', '')}"
    os.makedirs(output_dir, exist_ok=True)

    pdb_ids = fetch_released_pdb_ids(since_date)
    if not pdb_ids:
        return

    output_data = []
    for i, pdb_id in enumerate(pdb_ids, 1):
        print(f"Fetching metadata for {pdb_id} ({i}/{len(pdb_ids)})...")
        metadata = fetch_metadata(pdb_id, output_dir)
        if metadata:
            output_data.append(metadata)
        time.sleep(0.1)

    today_str = datetime.now().strftime('%Y-%m-%d')
    output_file = f"pdb_metadata_with_transmembrane_since_{since_date}_saved_{today_str}.csv"
    save_to_csv(output_data, output_file)

if __name__ == "__main__":
    main()
