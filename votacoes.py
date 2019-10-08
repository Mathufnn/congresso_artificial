import xml.etree.ElementTree as ET

class Votacao:
  def __init__(self, data="", cod=0, sigla="", casa="", secreta="", res="", votos={}, total_sim=0, total_nao=0, ano="", desc=""):
    self.data_sessao = data       # string formato aaaa-mm-dd
    self.codigo_sessao = cod      # inteiro formado por cast de string
    self.sigla_materia = sigla    # string, sigla referente a materia votada (Ex. PEC, MSF)
    self.casa = casa              # casa onde foi votada a sessao
    self.secreta = secreta        # string com valores S ou N (secreta ou nao-secreta)
    self.resultado = res          # string com valores A ou R (materia aprovada ou reprovada)
    self.votos = votos            # dicionario que relaciona numero do senador com o valor do voto (sim, nao, ausente, nao registrou, etc)
    self.total_votos_sim = total_sim  # inteiro formado por cast de string
    self.total_votos_nao = total_nao  # inteiro formado por cast de string
    self.ano_materia = ano        # string em formato aaaa
    self.descricao = desc         # string grande com descricao da votacao da materia

lista_votacoes = []               # lista de instancias da classe Votacao, para ser exportada para outro arquivo

for i in range(1991, 2018):       # itera sobre os anos dos arquivos XML das votacoes e faz o parsing do xml
  root = ET.parse("lista_votacoes_xml/lista_votacoes" + str(i) + ".xml").getroot()

  for votacao_element in root[1].findall("Votacao"):
    data1 = votacao_element.find("DataSessao").text
    codigo1 = int(votacao_element.find("CodigoSessao").text)
    sigla1 = votacao_element.find("SiglaMateria")
    casa1 = votacao_element.find("SiglaCasa").text
    secreta1 = votacao_element.find("Secreta").text
    resultado1 = votacao_element.find("Resultado")

    votos = {}
    for voto in votacao_element.iter("Votos"):
      codigo_parl = voto.find("CodigoParlamentar")
      voto_parl = voto.find("Voto")
      votos[codigo_parl] = voto_parl

    total_votos_sim1 = votacao_element.find("TotalVotosSim")
    # if total_votos_sim1 is not None:
    #   total_votos_sim1 = int(total_votos_sim1)

    total_votos_nao1 = votacao_element.find("TotalVotosNao")
    # if total_votos_nao1 is not None:
    #   total_votos_nao1 = int(total_votos_nao1)

    ano_materia1 = votacao_element.find("AnoMateria")
    descricao1 = votacao_element.find("DescricaoVotacao").text
    
    instancia_votacao = Votacao(data1, codigo1, sigla1, casa1, secreta1, resultado1, votos, total_votos_sim1, total_votos_sim1, ano_materia1, descricao1)
    lista_votacoes.append(instancia_votacao)    # atribui os valores do arquivo XML à instancias da classe

num_instancias = len(lista_votacoes)
sigla_materia_ausente = 0
resultado_ausente = 0
votos_nao_ausente = 0
votos_sim_ausente = 0
ano_materia_ausente = 0

for votacao in lista_votacoes:
  if(votacao.sigla_materia is None):
    sigla_materia_ausente += 1
    # votacao.sigla_materia = ""
    # print("corrigido sigla")

  if (votacao.resultado is None):
    resultado_ausente += 1
    # votacao.resultado = ""
    # print("corrigido resultado")

  if (votacao.total_votos_sim is None):
    votos_sim_ausente += 1
    # votacao.total_votos_sim = ""
    # print("corrigido votos SIM")

  if (votacao.total_votos_nao is None):
    votos_nao_ausente += 1
    # votacao.total_votos_nao = ""
    # print("corrigido votos NAO")

  if (votacao.ano_materia is None):
    ano_materia_ausente += 1
    # votacao.ano_materia = ""
    # print("corrigido ano materia")

print("Votacoes com sigla ausente: ", sigla_materia_ausente, sigla_materia_ausente/num_instancias)
print("Votacoes com resultado ausente: ", resultado_ausente, resultado_ausente/num_instancias)
print("Votacoes com votos nao ausente: ", votos_nao_ausente, votos_nao_ausente/num_instancias)
print("Votacoes com votos sim ausente: ", votos_sim_ausente, votos_sim_ausente/num_instancias)
print("Votacoes com ano ausente: ", ano_materia_ausente, ano_materia_ausente/num_instancias)