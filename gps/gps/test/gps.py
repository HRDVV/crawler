"""
 Created by hanruida on 2019-03-23
"""
import xlrd


class TestExcel:
    def __init__(self, filename):
        self.wb = xlrd.open_workbook(filename=filename)

    def read_excel(self):
        print(self.wb.sheet_by_index(0).col_values(0))


xl = TestExcel("../input/gps.xlsx")
xl.read_excel()
