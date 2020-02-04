import xlrd     # biblioteca para parsing de arquivos .xlsx

class PEC:
  def __init__(self, num="", ass="", just="", res=""):
    self.numero = num
    self.assunto = ass
    self.descricao = just
    self.resultado = res
  def __repr__(self):
    return "Número: %s, Assunto: %s, Resultado: %s \n" % (self.numero, self.assunto, self.resultado)
  
xl_workbook = xlrd.open_workbook("PECs.xlsx")
lista_pecs = []

for xl_sheet in xl_workbook.sheets():
  for row_idx in range(1, xl_sheet.nrows):
    temp_pec = []
    for col_idx in range(0, xl_sheet.ncols):
      temp_pec.append(xl_sheet.cell(row_idx, col_idx).value)
      print(col_idx)
    pec = PEC(temp_pec[0], temp_pec[1], temp_pec[2], temp_pec[4])
    lista_pecs.append(pec)

print(lista_pecs)