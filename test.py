import requests

response = requests.get('http://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista?ano=2013')
with open('teste.xml', 'wb') as file:
  file.write(response.content)