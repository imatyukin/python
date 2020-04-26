#!/usr/bin/env python3
# 4. Modify csv2html.py again, this time adding a new function called process_
#    options(). This function should be called from main() and should
#    return a tuple of two values: maxwidth (an int) and format (a str). When
#    process_options() is called it should set a default maxwidth of 100, and a
#    default format of “.0f”—this will be used as the format specifier when outputting
#    numbers.
#
#    If the user has typed “-h” or “--help” on the command line, a usage message
#    should be output and (None, None) returned. (In this case main() should
#    do nothing.) Otherwise, the function should read any command-line
#    arguments that are given and perform the appropriate assignments. For
#    example, setting maxwidth if “maxwidth=n” is given, and similarly setting
#    format if “format=s” is given. Here is a run showing the usage output:
#
#        csv2html2_ans.py -h
#        usage:
#        csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html
#
#        maxwidth is an optional integer; if specified, it sets the maximum
#        number of characters that can be output for string fields,
#        otherwise a default of 100 characters is used.
#
#        format is the format to use for numbers; if not specified it
#        defaults to ".0f".
#
#    And here is a command line with both options set:
#
#        csv2html2_ans.py maxwidth=20 format=0.2f < mydata.csv > mydata.html
#
#    Don’t forget to modify print_line() to make use of the format for outputting
#    numbers—you’ll need to pass in an extra argument, add one line,
#    and modify another line. And this will slightly affect main() too. The process_
#    options() function should be about twenty-five lines (including about
#    nine for the usage message). This exercise may prove challenging for inexperienced
#    programmers.
#
#    Two files of test data are provided: data/co2-sample.csv and data/co2-from-fossilfuels.
#    csv. A solution is provided in csv2html2_ans.py. In Chapter 5
#    we will see how to use Python’s optparse module to simplify command-line
#    processing.

import sys
import xml.sax.saxutils


def main():
    maxwidth, format = process_options()
    if maxwidth is not None:
        print_start()
        count = 0
        while True:
            try:
                line = input()
                if count == 0:
                    color = "lightgreen"
                elif count % 2:
                    color = "white"
                else:
                    color = "lightyellow"
                print_line(line, color, maxwidth, format)
                count += 1
            except EOFError:
                break
        print_end()


def print_start():
    print("<table border='1'>")


def print_line(line, color, maxwidth, format):
    print("<tr bgcolor='{0}'>".format(color))
    numberFormat = "<td align='right'>{{0:{0}}}</td>".format(format)
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print(numberFormat.format(x))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                if len(field) <= maxwidth:
                    field = xml.sax.saxutils.escape(field)
                else:
                    field = "{0} ...".format(
                            xml.sax.saxutils.escape(field[:maxwidth]))
                print("<td>{0}</td>".format(field))
    print("</tr>")


def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None: # start of quoted string
                quote = c
            elif quote == c:  # end of quoted string
                quote = None
            else:
                field += c    # other quote inside quoted string
            continue
        if quote is None and c == ",": # end of a field
            fields.append(field)
            field = ""
        else:
            field += c        # accumulating a field
    if field:
        fields.append(field)  # adding the last field
    return fields


def escape_html(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def print_end():
    print("</table>")


def process_options():
    maxwidth_arg = 'maxwidth='
    format_arg = 'format='
    maxwidth = 100
    format = ".0f"
    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            print('''usage:
csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html

maxwidth is an optional integer; if specified, it sets the maximum
number of characters that can be output for string fields,
otherwise a default of 100 characters is used.
(maxwidth - необязательное целое число. Если задано, определяет
максимальное число символов для строковых полей. В противном случае
используется значение по умолчанию 100.)

format is the format to use for numbers; if not specified it
defaults to ".0f".
(format - формат вывода чисел. Если не задан, по умолчанию используется
формат ".0f".)''')
            return None, None
        elif arg.startswith(maxwidth_arg):
            try:
                maxwidth = int(arg.split('=')[1])
            except ValueError:
                pass
        elif arg.startswith(format_arg):
            format = str(arg.split('=')[1])
    return maxwidth, format


main()
