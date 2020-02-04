import xml.etree.ElementTree as ET

class Votacao:
  def __init__(self, data="", cod=0, sigla="", casa="", secreta="", res="", votos={}, total_sim=0, total_nao=0, ano="", desc="", desc_ident=""):
    self.data_sessao = data       # string formato aaaa-mm-dd
    self.codigo_sessao = cod      # inteiro formado por cast de string
    self.sigla_materia = sigla    # string, sigla referente a materia votada (Ex. PEC, MSF)
    self.casa = casa              # string, referente a casa onde foi votada a sessao
    self.secreta = secreta        # string com valores S ou N (secreta ou nao-secreta)
    self.resultado = res          # string com valores A ou R (materia aprovada ou reprovada)
    self.votos = votos            # dicionario que relaciona numero do senador com o valor do voto (sim, nao, ausente, nao registrou, etc)
    self.total_votos_sim = total_sim  # inteiro formado por cast de string
    self.total_votos_nao = total_nao  # inteiro formado por cast de string
    self.ano_materia = ano        # string em formato aaaa
    self.descricao = desc         # string grande com descricao da votacao da materia
    self.descricao_identificacao = desc_ident  # string que identifica as materias pelo indice
  
  def __repr__(self):
    return "Data: %s, Codigo: %s, Resultado: %s \n" % (self.data_sessao, self.codigo_sessao, self.resultado)

lista_votacoes = []               # lista de instancias da classe Votacao, pode ser exportada para outro arquivo

def trata_dado_ausente(elemento):# funcao para tratar objetos do tipo "NoneType" que aparecem quando
  var = elemento                  # ha dados ausentes, quando o elemento e uma string.
  if(elemento is None):           # caso o elemento seja NoneType, atribui-se uma string vazia a ele
    var = ""
  else:                           # caso contrario, ele recebe o conteudo do elemento a que pertence
    var = var.text
  return var

def trata_dado_ausente_int(elemento):  # trata objetos "NoneType" e substitui-os por numeros
  var = elemento
  if(elemento is None):
    var = 0
  else:
    var = int(var.text)
  return var

for i in range(1991, 2018):       # itera sobre os anos dos arquivos XML das votacoes e faz o parsing do xml
  root = ET.parse("lista_votacoes_xml/lista_votacoes" + str(i) + ".xml").getroot()

  for votacao_element in root[1].findall("Votacao"):
    data1 = trata_dado_ausente(votacao_element.find("DataSessao"))
    codigo1 = trata_dado_ausente_int(votacao_element.find("CodigoSessao"))
    sigla1 = trata_dado_ausente(votacao_element.find("SiglaMateria"))
    casa1 = trata_dado_ausente(votacao_element.find("SiglaCasa"))
    secreta1 = trata_dado_ausente(votacao_element.find("Secreta"))
    resultado1 = trata_dado_ausente(votacao_element.find("Resultado"))

    votos = {}
    for voto in votacao_element.iter("Votos"):
      codigo_parl = voto.find("CodigoParlamentar")
      voto_parl = voto.find("Voto")
      votos[codigo_parl] = voto_parl

    total_votos_sim1 = trata_dado_ausente_int(votacao_element.find("TotalVotosSim"))
    total_votos_nao1 = trata_dado_ausente_int(votacao_element.find("TotalVotosNao"))
    ano_materia1 = trata_dado_ausente(votacao_element.find("AnoMateria"))
    descricao1 = trata_dado_ausente(votacao_element.find("DescricaoVotacao"))
    descricao_identificacao1 = trata_dado_ausente(votacao_element.find("DescricaoIdentificacaoMateria"))
    
    instancia_votacao = Votacao(data1, codigo1, sigla1, casa1, secreta1, resultado1, votos, total_votos_sim1, total_votos_sim1, ano_materia1, descricao1)
    lista_votacoes.append(instancia_votacao)    # atribui os valores do arquivo XML as instancias da classe

removidos = 0
pecs = 0
for votacao in lista_votacoes:
  if (votacao.resultado == ""):
    lista_votacoes.remove(votacao)
    removidos += 1

  if(votacao.sigla_materia == "PEC"):
    pecs += 1

print("Número de pecs: ", pecs)
print("Número de instâncias após remover as sem resultado: ", len(lista_votacoes))
print("Lista de votações gerada com sucesso.")