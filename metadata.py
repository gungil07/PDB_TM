import requests
from uniprot_utils import get_uniprot_ids_from_pdb, is_transmembrane

def fetch_metadata(pdb_id, save_dir):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch metadata for {pdb_id}")
        return None

    data = response.json()
    title = data.get("struct", {}).get("title", "")
    citation = data.get("rcsb_primary_citation", {})
    pubmed_id = citation.get("pdbx_database_id_pub_med", "")
    exptl = data.get("exptl", [{}])
    method = exptl[0].get("method", "") if exptl else ""
    resolution = data.get("rcsb_entry_info", {}).get("resolution_combined", [None])
    resolution_value = resolution[0] if resolution else None

    uniprot_ids = get_uniprot_ids_from_pdb(pdb_id)
    uniprot_str = ", ".join(uniprot_ids) if uniprot_ids else ""
    transmembrane = "Yes" if any(is_transmembrane(uid, save_dir) for uid in uniprot_ids) else "No"

    return {
        "PDB_ID": pdb_id,
        "Title": title,
        "PubMed_ID": pubmed_id,
        "Resolution (Å)": resolution_value,
        "Experimental Method": method,
        "UniProt_IDs": uniprot_str,
        "Transmembrane": transmembrane
    }