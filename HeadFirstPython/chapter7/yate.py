#!/usr/bin/env python3

'''Import the “Template” class from the standard library’s “string”
module. This allows for simple string-substitution templates.'''
from string import Template

'''This function takes a single (optional) string as its argument and uses it to
create a CGI “Content-type:” line, with “text/html” as the default.'''
def start_response(resp="text/html"):
    return('Content-type: ' + resp + '\n\n')

'''This function takes a single string as its argument and uses at the title for
the start of a HTML page. The page itself is stored within a separate file
in “templates/header.html”, and the title is substituted in as needed.'''
def include_header(the_title):
    with open('templates/header.html') as headf:
        head_text = headf.read()
    header = Template(head_text)
    return(header.substitute(title=the_title))

'''Similar to the “include_header” function, this one uses its single string as
its argument to create the end of a HTML page. The page itself is stored
within a separate file in “templates/footer.html”, and the argument is used
to dynamically create a set of HTML link tags. Based on how they are used,
it looks like the argument needs to be a dictionary.'''
def include_footer(the_links):
    with open('templates/footer.html') as footf:
        foot_text = footf.read()
    link_string = ''
    for key in the_links:
        link_string += '<a href="' + the_links[key] + '">' + key + '</a>&nbsp;&nbsp;&nbsp;&nbsp;'
    footer = Template(foot_text)
    return(footer.substitute(links=link_string))

'''This function returns the HTML for the start of a form and lets the caller
specify the URL to send the form’s data to, as well as the method to use.'''
def start_form(the_url, form_type="POST"):
    return('<form action="' + the_url + '" method="' + form_type + '">')

'''This function returns the HTML markup, which terminates the form while
allowing the caller to customize the text of the form’s “submit” button.'''
def end_form(submit_msg="Submit"):
    return('<p></p><input type=submit value="' + submit_msg + '">')

'''Given a radio-button name and value, create a HTML radio button (which is
typically included within a HTML form). Note: both arguments are required.'''
def radio_button(rb_name, rb_value):
    return('<input type="radio" name="' + rb_name + '" value="' + rb_value + '"> ' + rb_value + '<br />')

'''Given a list of items, this function turns the list into a HTML unnumbered
list. A simple “for” loop does all the work, adding a LI to the UL element
with each iteration.'''
def u_list(items):
    u_string = '<ul>'
    for item in items:
        u_string += '<li>' + item + '</li>'
    u_string += '</ul>'
    return(u_string)

'''Create and return a HTML header tag (H1, H2, H2, and so on) with level 2
as the default.. The “header_text” argument is required.'''
def header(header_text, header_level=2):
    return('<h' + str(header_level) + '>' + header_text + '</h' + str(header_level) + '>')

'''Enclose a paragraph of text (a string) in HTML paragraph tags.'''
def para(para_text):
    return('<p>' + para_text + '</p>')
