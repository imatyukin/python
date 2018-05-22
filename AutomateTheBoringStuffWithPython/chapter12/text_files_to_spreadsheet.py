#!/usr/bin/env python3
import openpyxl
import os

def main():

    path = "."
    text_files = [f for f in os.listdir(path) if f.endswith(".txt")]

    wb = openpyxl.Workbook()
    sheet = wb.active

    for col, text_file in enumerate(text_files):
        with open(text_file, 'rb') as f:
            lines = f.readlines()
        print(lines)
        for row, line in enumerate(lines):
            sheet.cell(row=row+1, column=col+1).value = line

    wb.save('text_to_spreadsheet.xlsx')


if __name__ == "__main__":
    main()
