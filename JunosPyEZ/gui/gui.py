#!/usr/bin/env python3
''' The GUI for the PyEZ Script:
Output of PyEZ device "facts", BGP summary information, Interfaces' state information. '''
from tkinter import *   # import all tkinter objects, such as Tk, Frame, Label, etc.
from jnpr.junos import Device
from jnpr.junos.exception import *
from pprint import pformat

# Can be changed by user at the script run-time.
USER = 'lab'
PASSWD = 'lab123'
DEVICE_IP = '127.0.0.1'

def output(st):
    ''' The text object '''
    text.insert(END, chars=st) # adds characters to the end of the output
    text.see(END) # scrolls the output to the end

def read_and_display(message, function):
    ''' The connection to the Junos device '''
    output(message)
    try:
        with Device(host=entry_dev.get(), user=entry_user.get(),
                    password=entry_pw.get()) as dev:
            res = function(dev)
    except ConnectRefusedError:
        print("\nError: Connection refused!\n")
    except ConnectTimeoutError:
        output("\nConnection timeout error!\n")
    except ConnectUnknownHostError:
        output("\nError: Connection attempt to unknown host.\n")
    except ConnectionError:
        output("\nConnection error!\n")
    except ConnectAuthError:
        output("\nConnection authentication error!\n")
    else:
        output(res)

def print_facts():
    ''' Junos PyEZ device facts '''
    read_and_display("\nDevice facts:\n", lambda dev: pformat(dev.facts))

def show_bgp():
    ''' show bgp summary '''
    read_and_display("\nBGP summary information:",
                     lambda dev: dev.rpc.get_bgp_summary_information({"format": "text"}).text)

def show_intf():
    ''' show interfaces terse '''
    read_and_display("\nInterface information:",
                     lambda dev: dev.rpc.get_interface_information({"format": "text"}, terse=True).text)

def main():

    # User entry text fields and the output text object.
    global entry_dev, entry_user, entry_pw, text
    # The main window, everything else is placed inside it.
    root = Tk()

    # Create an unnamed frame and put it to the grid in the 0-th row.
    Frame(root, height=10).grid(row=0)

    # Create a Label (with output text "Device address:") and put it into the grid in row 1, column 0.
    Label(root, text="Device address:").grid(row=1, column=0)
    # Create a user entry field named entry_dev to be used for entering the device IP address.
    # Put it on the grid and use DEVICE_IP as a default value.
    entry_dev = Entry(root)
    entry_dev.grid(row=1, column=1)
    entry_dev.insert(END, DEVICE_IP)

    # Create a label and an entry field for the username.
    Label(root, text="Login:").grid(row=2, column=0)
    entry_user = Entry(root)
    entry_user.grid(row=2, column=1)
    entry_user.insert(END, USER)

    # Create a label and an entry field for the password.
    # Argument show="*" ensures that password is not displayed.
    Label(root, text="Password:").grid(row=3, column=0)
    entry_pw = Entry(root, show="*")
    entry_pw.grid(row=3, column=1)
    entry_pw.insert(END, PASSWD)

    # Create a couple of empty frames and three buttons, and put all that into the grid.
    Frame(root, height=10).grid(row=4)
    Button(root, text="Read facts!", command = print_facts).grid(row=5, column=0)
    Button(root, text="Show interfaces!", command = show_intf).grid(row=5, column=1)
    Button(root, text="Show BGP!", command = show_bgp).grid(row=5, column=2)
    Frame(root, height=10).grid(row=6)

    # Create another frame with a specified size, this time giving it a name (frame) and putting a text field text inside it.
    frame = Frame(root, width=800, height=700)
    frame.grid(row=7, column=0, columnspan=4)
    frame.grid_propagate(False)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    text = Text(frame, borderwidth=3)
    text.config(font=("courier", 11), wrap ='none')
    text.grid(row=0, column=0, sticky="nsew", padx = 2, pady = 2)

    # Attach X and Y scrollbars to the text field.
    scrollbarY = Scrollbar(frame, command=text.yview)
    scrollbarY.grid(row=0, column=1, sticky='nsew')
    text['yscrollcommand'] = scrollbarY.set
    scrollbarX = Scrollbar(frame, orient=HORIZONTAL, command=text.xview)
    scrollbarX.grid(row=1, column=0, sticky='nsew')
    text['xscrollcommand'] = scrollbarX.set

    # Display the main window by calling the mainloop() method.
    root.mainloop()

if __name__ == "__main__":
    main()