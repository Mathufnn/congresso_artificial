import os
indice, pagina, ano = 8, 44, 2012
print(os.stat("lista_materias_pdf/" + str(ano) + "/" + "materia" + str(indice) + "_pag" + str(pagina) + "_ano" + str(ano) + ".pdf").st_size)
