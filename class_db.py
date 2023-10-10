import sqlite3
import openpyxl

dataframe1 = openpyxl.load_workbook('/Users/Archith/Downloads/Class_list.xlsx')
dataframe1 = dataframe1.active
m_row = dataframe1.max_row

print(dataframe1.columns)

