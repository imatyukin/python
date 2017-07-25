#!/usr/bin/env python3

from yate import *

'''start_response()'''
'''The CGI standard states that every web response must start with a header line that
indictes the type of the data included in the request'''
print(start_response())
print(start_response("text/plain"))
print(start_response("application/json"))

print('\n================================ RESTART ================================\n')

'''include_header()'''
'''The function generates the start of a web page and let’s you customizee its title'''
print(include_header("Welcome to my home on the web!"))

print('\n================================ RESTART ================================\n')

'''include_footer()'''
'''The function produces HTML that terminates a web page, providing links (if provided as a
dictionary)'''
print(include_footer({'Home': '/index.html', 'Select': '/cgi-bin/select.py'}))
print(include_footer({}))

print('\n================================ RESTART ================================\n')

'''start_form() and end_form()'''
'''The functions bookend a HTML form, with the parameter (if supplied) adjusting the contents 
of the generated HTML'''
print(start_form("/cgi-bin/process-athlete.py"))
print(end_form())
print(end_form("Click to Confirm Your Order"))

print('\n================================ RESTART ================================\n')

'''radio_button()'''
'''HTML radio buttons are easy to create with the function'''
for fab in ['John', 'Paul', 'George', 'Ringo']:
    print(radio_button(fab, fab))

print('\n================================ RESTART ================================\n')

'''u_list()'''
'''Unordered list are function'''
print(u_list(['Life of Brian', 'Holy Grail']))

print('\n================================ RESTART ================================\n')

'''header()'''
'''The function lets you quickly format HTML headings at a selected level (with 2 as the default)'''
print(header("Welcome to my home on the web"))
print(header("This is a sub-sub-sub-sub heading", 5))

print('\n================================ RESTART ================================\n')

'''para()'''
'''The function encloses a chunk of text within HTML paragraph tags'''
print(para("Was it worth the wait? We hope it was..."))

