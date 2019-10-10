import xlrd     # biblioteca para parsing de arquivos .xlsx

class PEC:
  def __init__(self, num="", ass="", desc="", aut="", res=""):
    self.numero = num
    self.assunto = ass
    self.descricao = desc
    self.autoria = aut
    self.resultado = res
  def __repr__(self):
    return "Número: %s, Assunto:%s, Resultado:%s \n" % (self.numero, self.assunto, self.resultado)
  
xl_workbook = xlrd.open_workbook("PEC_s.xlsx")
sheet_names = xl_workbook.sheet_names()
xl_sheet = xl_workbook.sheet_by_name(sheet_names[1])

lista_pecs = []

for row_idx in range(1, xl_sheet.nrows):
  temp_pec = []
  for col_idx in range(0, xl_sheet.ncols):
    temp_pec.append(xl_sheet.cell(row_idx, col_idx).value)
  pec = PEC(temp_pec[0], temp_pec[1], temp_pec[2], temp_pec[3], temp_pec[4])
  lista_pecs.append(pec)

print(lista_pecs)