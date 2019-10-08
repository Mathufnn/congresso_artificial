import requests

response = requests.get('http://legis.senado.leg.br/dadosabertos/senador/lista/atual')
with open('lista.xml', 'wb') as file:
  file.write(response.content)