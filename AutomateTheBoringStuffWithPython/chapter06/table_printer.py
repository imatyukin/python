#!/usr/bin/env python3


def main():
    tableData = [['apples', 'oranges', 'cherries', 'banana'],
                 ['Alice', 'Bob', 'Carol', 'David'],
                 ['dogs', 'cats', 'moose', 'goose']]

    printTable(tableData)


def printTable(tableData):
    num_cols = len(tableData[0])
    col_widths = [largestElement(i) for i in tableData]

    for element in range(num_cols):
        row = ""
        for col, inner_list in enumerate(tableData):
            row += inner_list[element].rjust(col_widths[col]) + " "
        print(row)


def largestElement(mylist):
    return len(max(mylist, key=len))


if __name__ == "__main__":
    main()
