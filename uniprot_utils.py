import requests
import os

def get_uniprot_ids_from_pdb(pdb_id):
    url = f"https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{pdb_id.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    if pdb_id.lower() not in data or 'UniProt' not in data[pdb_id.lower()]:
        return []

    return list(data[pdb_id.lower()]['UniProt'].keys())

def is_transmembrane(uniprot_id, save_dir):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.txt"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{uniprot_id}: Failed to retrieve UniProt entry")
        return False

    entry_text = response.text
    with open(os.path.join(save_dir, f"{uniprot_id}.txt"), "w") as f:
        f.write(entry_text)

    for line in entry_text.splitlines():
        if line.startswith("FT   TRANSMEM") or "Transmembrane" in line:
            return True
    return False