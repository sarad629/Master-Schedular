import pandas as pd
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def open_class_list():
    path = "/Users/Archith/Downloads/Class_list.xlsx"
    df = pd.read_excel(path)

    for row in range(0, len(df)):
        row_list = df.iloc[row].tolist()
        available_class = row_list[0]
        period1 = int(row_list[1])
        period2 = int(row_list[2])
        period3 = int(row_list[3])
        period4 = int(row_list[4])
        period5 = int(row_list[5])
        period6 = int(row_list[6])
        period7 = int(row_list[7])
        period8 = int(row_list[8])

        conn = get_db_connection()
        conn.execute('INSERT INTO classes (class, period1, period2, period3, period4, period5, period6, period7, '
                     'period8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (available_class, period1, period2, period3, period4,
                      period5, period6, period7, period8))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    open_class_list()
