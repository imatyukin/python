#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

parser = ArgumentParser(description='Currencies')
parser.add_argument('command', type=str,
                    help='what to do')
parser.add_argument('--filename', '-f', type=str,
                    dest='filename',
                    default='course.csv',
                    help='name of file' )
                    
args = parser.parse_args()
if args.command == 'get':
    import get
    get.get(args.filename)
elif args.command == 'show':
    import show_data
    show_data.show(args.filename)
