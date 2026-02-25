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
from config import DNA_URL, SCI_URL, ACC_URL



def get_animal_info(common) -> dict[str: str]:
    """
    Retrieves the scientific name and DNA sequence for a given common animal name.

    Args:
        common (str): The common name of the animal.

    :return
        dict[str: str]: A dictionary containing the common name, scientific name, accession number, and DNA sequence of the animal.
        If any errors occur during the API calls or JSON parsing, the scientific name, accession number, and DNA sequence will be set to "N/A".
    """


    try:
        url = SCI_URL + common


        response = requests.get(url)
        response.raise_for_status()

        data_scientific = response.json()
        print(data_scientific)
        if not data_scientific:
            return None
        else:
            scientific_name = data_scientific[0]["scientificName"]
            tax_id = data_scientific[0]["taxId"]

            url = ACC_URL

            params = {
                "result": "sequence",
                "query": f"tax_eq({tax_id})",
                "fields": "accession",
                "format": "json",
                "limit": 1
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data_acc = response.json()
            accession = data_acc[0]["accession"]


            url = DNA_URL + accession

            response = requests.get(url)
            response.raise_for_status()

            dna_sequence =  response.text

            dna_sequence = dna_sequence.split("\n")
            dna_sequence = "".join(dna_sequence[1:])

            # print(dna_sequence)

            animal_info = {
                "common_name": common,
                "scientific_name": scientific_name,
                "accession": accession,
                "dna_sequence": dna_sequence
            }

            return animal_info


    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {
            "common_name": common,
            "scientific_name": "N/A",
            "accession": "N/A",
            "dna_sequence": "N/A"
        }

    except json.decoder.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {
            "common_name": common,
            "scientific_name": "N/A",
            "accession": "N/A",
            "dna_sequence": "N/A"
        }