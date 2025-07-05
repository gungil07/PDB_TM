import requests
import csv

def fetch_released_pdb_ids(since_date):
    url = "https://search.rcsb.org/rcsbsearch/v2/query"
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_accession_info.initial_release_date",
                "operator": "greater_or_equal",
                "value": since_date
            }
        },
        "return_type": "entry",
        "request_options": {
            "return_all_hits": True
        }
    }

    response = requests.post(url, json=query)
    if response.status_code != 200:
        print(f"Failed to fetch from RCSB ({response.status_code})")
        return []

    data = response.json()
    pdb_ids = [item["identifier"] for item in data.get("result_set", [])]
    print(f"Found {len(pdb_ids)} PDB entries since {since_date}")
    return pdb_ids

def save_to_csv(pdb_data_list, output_file):
    fieldnames = ["PDB_ID", "Title", "PubMed_ID", "Resolution (Å)", "Experimental Method", "UniProt_IDs", "Transmembrane"]
    with open(output_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in pdb_data_list:
            writer.writerow(row)
    print(f"Metadata saved to: {output_file}")
