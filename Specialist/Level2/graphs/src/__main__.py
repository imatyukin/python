#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from by_width import by_width2, by_width
from by_depth import by_depth

graph = {
    'A' : [ 'B', 'F' ],
    'B' : [ 'C', 'D' ],
    'C' : [ 'F' ],
    'D' : [ 'C', 'E', 'G' ],
    'E' : [],
    'F' : [ 'D', 'G', 'S' ],
    'G' : [ 'C', 'E', 'S' ],
    'S' : [ 'E' ],
    'T' : [ 'A' ]
}

for way in by_depth(graph, 'A', 'E'):
    print(way)
