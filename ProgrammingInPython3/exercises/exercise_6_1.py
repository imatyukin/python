#!/usr/bin/env python3
# 1. Modify the Point class (from Shape.py or ShapeAlt.py), to support the
#    following operations, where p, q, and r are Points and n is a number:
#
#        p = q + r   # Point.__add__()
#        p += q      # Point.__iadd__()
#        p = q - r   # Point.__sub__()
#        p -= q      # Point.__isub__()
#        p = q * n   # Point.__mul__()
#        p *= n      # Point.__imul__()
#        p = q / n   # Point.__truediv__()
#        p /= n      # Point.__itruediv__()
#        p = q // n  # Point.__floordiv__()
#        p //= n     # Point.__ifloordiv__()
#
#    The in-place methods are all four lines long, including the def line, and
#    the other methods are each just two lines long, including the def line,
#    and of course they are all very similar and quite simple. With a minimal
#    description and a doctest for each it adds up to around one hundred thirty
#    new lines. A model solution is provided in Shape_ans.py; the same code is
#    also in ShapeAlt_ans.py.

