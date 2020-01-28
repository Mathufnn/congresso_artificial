import PyPDF2
indice, pagina, ano = 8, 21, 2014
pdfFileObj = open("lista_materias_pdf/" + str(ano) + "/" + "materia" + str(indice) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
for i in range(0, pdfReader.getNumPages()):
  print(pdfReader.getPage(i).extractText())
