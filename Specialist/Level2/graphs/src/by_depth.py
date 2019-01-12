#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def by_depth(graph, start, finish):
    way = [ start ]
    nei = [ list(graph[start]) ]
    while way:
        n = nei[-1]
        for vertex in list(n):
            if vertex == finish:
                yield way + [vertex]
                n.remove(vertex)
            elif vertex in way:
                n.remove(vertex)
            else:
                n.remove(vertex)
                way.append(vertex)
                nei.append( list(graph[vertex]) )
                break
        else:
            del way[-1]
            del nei[-1]
