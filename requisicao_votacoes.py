import requests

for i in range(1991, 2018):
  response = requests.get('http://legis.senado.leg.br/dadosabertos/dados/ListaVotacoes' + str(i) + '.xml')
  
  with open("lista_votacoes_xml/lista_votacoes" + str(i) + ".xml", "w", encoding="utf-8") as file:
    file.write(response.text)