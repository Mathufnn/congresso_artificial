import re
import os.path
import unicodedata
from io import StringIO
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# Esse script foi feito para preprocessar os PDFs das materias do senado de 2007 ate 2019.
# Requer que os PDFs ja tenham sido baixados usando o script "scraping_materias.py".
# O preprocessamento e feito transformando os PDFs em strings de texto puro em TXTs, e removendo
# caracteres especiais, ou seja, caracteres nao alfanumericos.

# alguns PDFs tem tamanho grande demais para serem processados pela biblioteca PDFminer,
# portanto o tamanho maximo dos PDFs a serem usados sera 5 MB.
MAX_FILE_SIZE = 5000000 # 5 MB

# funcao que recebe como parametro o caminho do PDF e gera como saida a string presente no PDF
# usando a biblioteca PDFminer com a funcao interpreter.process_page().
def convert_pdf_to_txt(path):
  rsrcmgr = PDFResourceManager()
  retstr = StringIO()
  codec = 'utf-8'
  laparams = LAParams()
  device = TextConverter(rsrcmgr, retstr, laparams=laparams)
  fp = open(path, 'rb')
  interpreter = PDFPageInterpreter(rsrcmgr, device)
  password = ""
  maxpages = 0
  caching = True
  pagenos=set()

  for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
    interpreter.process_page(page)

  text = retstr.getvalue()
  fp.close()
  device.close()
  retstr.close()
  return text

# Funcao que recebe a string do texto do PDF extraida pelo PDFminer e gera como saida a string
# sem caracteres especiais.
# Existem casos em que o PDF nao possui texto e eh apenas um scan. nesse caso, alguns caracteres 
# de "lixo" podem aparecer, e, quando isso ocorre, geralmente possui menos de 200 caracteres.
# Para tratar esse problema, eh retornado uma string vazia para que isso seja tratado como um arquivo
# defeituoso posteriormente no codigo.
def limpar_texto(texto):
  if len(texto) < 200:
    return ""

  texto = texto.lower()
  nfkd = unicodedata.normalize('NFKD', texto)
  palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
  texto_limpo = re.sub('[^a-zA-Z0-9 \\\]', ' ', palavraSemAcento)
  texto_limpo = ' '.join(texto_limpo.split())

  return texto_limpo


for ano in range(checkpointano, 2020):
  for pagina in range(0,100):
    for indice in range(0,10):
      if(os.path.isfile("lista_materias_pdf/" + str(ano) + "/" + "materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf")):
        try:
          if os.stat("lista_materias_pdf/" + str(ano) + "/" + "materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf").st_size > MAX_FILE_SIZE:
            print("arquivo com tamanho invalido: ", "materia ", indice + 1, " da pagina ", pagina, " do ano ", ano)
            continue

          texto_puro = convert_pdf_to_txt("lista_materias_pdf/" + str(ano) + "/" + "materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf")
          texto_puro = limpar_texto(texto_puro)

          if not texto_puro:
            print("arquivo vazio: ", "materia ", indice + 1, " da pagina ", pagina, " do ano ", ano)

          else:
            with open("dataset_treinamento/" + "/" + "materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".txt", 'w') as file:
              file.write(texto_puro)
            print("preprocessado: ", "materia ", indice + 1, " da pagina ", pagina, " do ano ", ano)

        except PDFSyntaxError:
          print("erro no arquivo ", "materia ", indice + 1, " da pagina ", pagina, " do ano ", ano)
          with open("corrompidos.txt", "a") as file:
            file.write("materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf" + "\n")

        except TypeError:
          print("erro no arquivo ", "materia ", indice + 1, " da pagina ", pagina, " do ano ", ano)
          with open("corrompidos.txt", "a") as file:
            file.write("materia" + str(indice + 1) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf" + "\n")
