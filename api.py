"""
This module provides a function to retrieve animal information, including scientific name, accession number, and DNA
sequence, based on the common name of the animal. It interacts with external APIs to fetch the required data and handles potential exceptions that may arise during the process.

Functions:
- get_animal_info(common: str) -> dict[str: str]: Retrieves the scientific name
    and DNA sequence for a given common animal name.
    It makes API calls to fetch the scientific name, accession number, and DNA sequence, and returns this information in a dictionary format.
    If any errors occur during the API calls or JSON parsing, it returns a dictionary with "N/A" values for the scientific name, accession number, and DNA sequence.
"""

import json
import requests
import logging
from urllib.parse import quote_plus
from config import DNA_URL, SCI_URL, ACC_URL



def _find_key_in_json(obj, key_name):
    """
    Small helper to recursively search for the first occurrence of key_name
    in a nested dict/list structure and return its value or None.
    """
    if isinstance(obj, dict):
        if key_name in obj:
            return obj[key_name]
        for v in obj.values():
            found = _find_key_in_json(v, key_name)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = _find_key_in_json(item, key_name)
            if found is not None:
                return found
    return None

def get_animal_info(common) -> dict[str, str]:
    """
    Retrieves the scientific name and DNA sequence for a given common animal name.

    Args:
        common (str): The common name of the animal.

    :return
        dict[str: str]: A dictionary containing the common name, scientific name, accession number, and DNA sequence of the animal.
        If any errors occur during the API calls or JSON parsing, the scientific name, accession number, and DNA sequence will be set to "N/A".
    """


    logging.basicConfig(level=logging.INFO)
    try:
        # ensure common is safe for URL usage
        encoded_common = quote_plus(str(common).strip())
        url = SCI_URL + encoded_common

        logging.info("Searching scientific info with URL: %s", url)
        response = requests.get(url)
        response.raise_for_status()

        data_scientific = response.json()
        logging.debug("Scientific API response: %s", data_scientific)

        # Return consistent dict when nothing found
        if not data_scientific:
            logging.info("No scientific data found for: %s", common)
            return {
                "common_name": common,
                "scientific_name": "N/A",
                "accession": "N/A",
                "dna_sequence": "N/A"
            }

        # defensive extraction of scientific name and tax id
        if isinstance(data_scientific, list) and data_scientific:
            first = data_scientific[0]
        elif isinstance(data_scientific, dict):
            # some APIs return dict with results key
            first = _find_key_in_json(data_scientific, "results") or data_scientific
            if isinstance(first, list) and first:
                first = first[0]
        else:
            first = {}

        scientific_name = first.get("scientificName") or first.get("scientific_name") or "N/A"
        tax_id = first.get("taxId") or first.get("tax_id")

        if not tax_id:
            logging.info("No tax_id found for %s; returning N/A", common)
            return {
                "common_name": common,
                "scientific_name": scientific_name,
                "accession": "N/A",
                "dna_sequence": "N/A"
            }

        # Query accession endpoint using params (more robust) if ACC_URL expects params
        params = {
            "result": "sequence",
            "query": f"tax_eq({tax_id})",
            "fields": "accession",
            "format": "json",
            "limit": 1
        }
        logging.info("Querying accession with params: %s", params)
        response = requests.get(ACC_URL, params=params)
        response.raise_for_status()

        data_acc = response.json()
        logging.debug("Accession API response: %s", data_acc)

        # robust extraction of accession value
        accession = None
        # try common patterns
        if isinstance(data_acc, list) and data_acc:
            accession = _find_key_in_json(data_acc, "accession")
            if isinstance(data_acc[0], dict) and "accession" in data_acc[0]:
                accession = data_acc[0]["accession"]
        elif isinstance(data_acc, dict):
            accession = _find_key_in_json(data_acc, "accession")

        if not accession:
            logging.info("No accession found for tax_id %s", tax_id)
            return {
                "common_name": common,
                "scientific_name": scientific_name,
                "accession": "N/A",
                "dna_sequence": "N/A"
            }

        # build DNA URL safely (ensure separator)
        sep = "" if DNA_URL.endswith("/") else "/"
        url = f"{DNA_URL}{sep}{accession}"
        logging.info("Fetching DNA sequence from URL: %s", url)
        response = requests.get(url)
        response.raise_for_status()

        dna_sequence_text = response.text or ""
        # handle FASTA: if contains header starting with '>', strip first line
        lines = dna_sequence_text.splitlines()
        if lines and lines[0].startswith(">"):
            sequence = "".join(lines[1:])
        else:
            # if not FASTA, assume whole response is sequence or contains newlines
            sequence = "".join(lines)

        sequence = sequence.strip() or "N/A"

        animal_info = {
            "common_name": common,
            "scientific_name": scientific_name,
            "accession": accession,
            "dna_sequence": sequence
        }

        return animal_info

    except requests.exceptions.RequestException as e:
        logging.error("Request error: %s", e)
        return {
            "common_name": common,
            "scientific_name": "N/A",
            "accession": "N/A",
            "dna_sequence": "N/A"
        }

    except json.decoder.JSONDecodeError as e:
        logging.error("JSON decode error: %s", e)
        return {
            "common_name": common,
            "scientific_name": "N/A",
            "accession": "N/A",
            "dna_sequence": "N/A"
        }