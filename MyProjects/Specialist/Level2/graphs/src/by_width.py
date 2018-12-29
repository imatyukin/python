#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def by_width(graph, start, finish):
    candidates = [ [ start ] ]
    while candidates:
        way = candidates.pop()
        end = way[-1]
        for vertex in graph[end]:
            if vertex == finish:
                yield way + [ vertex ]
            elif vertex not in way:
                candidates.append( way + [vertex] )


def by_width2(graph, start, finish):
    candidates = [ [ start ] ]
    while candidates:
        way = candidates.pop()
        end = way[-1]
        if end == finish:
            yield way
        else:
            for vertex in graph[end]:
                if vertex not in way:
                    candidates.append( way + [vertex] )


















