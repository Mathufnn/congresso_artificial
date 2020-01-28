import requests
from bs4 import BeautifulSoup
import os.path

# Esse script baixa automaticamente todas as matérias no senado, muitas delas com
# as justificações. visto que são mais de 10000 PDFs, programei um esquema de retomar
# o download caso haja alguma interrupção.

# loop para encontrar o último arquivo salvo, pois eles são salvos na ordem
# crescente de ano, pagina e indice.
def encontra_ultimo_arquivo():
  for ano in reversed(range(2007, 2020)):
    for pagina in reversed(range(0,100)):
      for indice in reversed(range(1,11)):
        if(os.path.isfile("lista_materias_pdf/" + str(ano) + "/" + "materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf")):
          return ano, pagina, indice

ult_ano, ult_pagina, ult_indice = encontra_ultimo_arquivo()

# loop para iterar nos anos em que as matérias são feitas
for ano in range(2007, 2020):
  if(ano < ult_ano):                # para verificar se o ultimo arquivo salvo é
    print("pulando ano de ", ano)   # de um ano mais recente do que o que se está
    continue                        # tentando baixar. caso positivo, pule para este ano.

  # loop para iterar nas páginas  (pois todos os anos possuem 100 páginas contendo 10 materias)
  for pagina in range(0,100):       
    if(ano == ult_ano and pagina < ult_pagina):         # para verificar se deve-se pular páginas
      print("pulando pagina ", pagina, " do ano ", ano)
      continue

    # faz a requisição da página e faz o fetch do conteúdo HTML
    page = requests.get("http://www6g.senado.leg.br/busca/?portal=Atividade+Legislativa&colecao=Projetos+e+Mat%C3%A9rias+-+Proposi%C3%A7%C3%B5es&ordem=data&q=&ano=" + str(ano) + "&p=" + str(pagina))
    soup = BeautifulSoup(page.content, 'html.parser')

    # esse loop é responsável por buscar as 10 matérias presentes em uma página específica.
    # mais uma vez, é feita uma verificação se o arquivo já está baixado.
    for indice, div in enumerate(soup.find_all("div", {"class": "sf-busca-resultados-item"})):
      if(os.path.isfile("lista_materias_pdf/" + str(ano) + "/" + "materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf")):
        print("materia ", indice + 1, " da pagina ", pagina, " do ano ", ano, " ja baixada.")
        continue

      # encontra o elemento que possui o link intermediário
      link_element = div.find("h3").find("a")
      link = link_element['href']
      page2 = requests.get(link)
      soup2 = BeautifulSoup(page2.content, 'html.parser')

      # o elemento "a" a seguir se refere ao link para o PDF da matéria em questão.
      a = soup2.find("a", {"class": "btn btn-default btn-link borda"})

      # é feita uma verificação para o caso do layout da página ser diferente, por exemplo, se não existir
      # o elemento "a" mencionado anteriormente com o link.
      try:
        link_texto_materia = a['href']
      except TypeError:
        print("Pulando materia ", indice + 1, " da pagina ", pagina, " do ano ", ano, ", link para materia nao encontrado.")
        continue

      # se o link existir, é feita mais uma requisição para buscar a matéria, e ela é salva no formato PDF
      # dentro da pasta lista_materias_pdf
      page3 = requests.get(link_texto_materia)
      with open("lista_materias_pdf/" + str(ano) + "/" + "materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf", 'wb') as file:
        file.write(page3.content)
      print("materia ", indice + 1, " da pagina ", pagina, " do ano ", ano, " baixada com sucesso.")