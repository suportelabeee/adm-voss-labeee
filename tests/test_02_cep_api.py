import requests
from rich.pretty import pprint

link = "https://viacep.com.br/ws/{}/json/"
cep = "88037000" # CEP do LabEEE

formated = link.format(cep)
response = requests.get(formated)
pprint(response.json())

