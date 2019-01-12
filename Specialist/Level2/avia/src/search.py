#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from FlightWay import FlightWay


def by_width(flights, start, finish):
    candidates = []
    for flight in flights[start]:
        candidates.append(FlightWay(flight))
    while candidates:
        way = candidates.pop()
        fin = way[-1].finish
        for f in flights[fin]:
            if f.finish == finish:
                yield way + [f]
            else:
                if f.finish not in way:
                    candidates.append(way+[f])
