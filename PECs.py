import xlrd

class PEC:
  def __init__(self):
    self.numero = 0
    self.descricao = ""
    self.autoria = ""
    self.situacao = ""
  

xl_workbook = xlrd.open_workbook("PEC_s.xlsx")
sheet_names = xl_workbook.sheet_names()
xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])

num_cols = xl_sheet.ncols   # Number of columns
for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
  print ('-'*40)
  print ('Row: %s' % row_idx)   # Print row number
  for col_idx in range(0, num_cols):  # Iterate through columns
    cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
    print ('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj))