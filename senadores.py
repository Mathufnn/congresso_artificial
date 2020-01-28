import xml.etree.ElementTree as ET

class Parlamentar:
  def __init__(self, codigo = 0, nome = "", partido = "", UF = "", ini = "", fim = ""):
    self.codigo = codigo
    self.nome = nome
    self.partido = partido
    self.UF = UF
    self.inicio_mandato = ini
    self.fim_mandato = fim
  def __repr__(self):
    return "Nome: %s, Partido: %s, UF: %s, Codigo:%d \n" % (self.nome, self.partido, self.UF, self.codigo)
  

root = ET.parse("lista_parlamentares.xml").getroot()
lista_parlamentares = []

for parlamentar_element in root[1].findall("Parlamentar"):
  identificacao_parlamentar = parlamentar_element.find("IdentificacaoParlamentar")
  mandato_parlamentar = parlamentar_element.find("Mandato")

  codigo = int(identificacao_parlamentar.find("CodigoParlamentar").text)
  nome = identificacao_parlamentar.find("NomeParlamentar").text
  partido = identificacao_parlamentar.find("SiglaPartidoParlamentar").text
  uf = identificacao_parlamentar.find("UfParlamentar").text

  lista_parlamentares.append(Parlamentar(codigo, nome, partido, uf))
      
# print(lista_parlamentares)