import requests

from config import DNA_URL, SCI_URL, ACC_URL

def scientific_name():

    common = input("Enter the common name of the animal: ")

    url = SCI_URL + common


    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data[0]["scientificName"], data[0]["taxId"]

def accession_number(tax_id):

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

    data = response.json()
    return data[0]["accession"]


def dna_sequence(accession):

    url = DNA_URL + accession

    response = requests.get(url)
    response.raise_for_status()

    return response.text

def get_dna_from_common_name():
    return dna_sequence(accession_number(scientific_name()))


sci, tax = scientific_name()

acc = accession_number(tax)

dna = dna_sequence(acc)

print(sci, tax)
print(acc)
print(dna[:200])