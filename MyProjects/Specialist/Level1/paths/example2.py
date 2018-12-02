#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os.path import join

root = 'C:\\'

os.walk(root)
for path, dirs, files in os.walk(root):
    if 'Program Files' in dirs:
        dirs.remove('Program Files')
    for f in files:
        file_path = join(path, f)
        print(file_path)