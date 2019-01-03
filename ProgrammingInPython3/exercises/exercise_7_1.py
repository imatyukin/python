#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 1. Make a new, simpler version of the BinaryRecordFile module—one that
#    does not use a state byte. For this version the record size specified by
#    the user is the record size actually used. New records must be added using
#    a new append() method that simply moves the file pointer to the end
#    and writes the given record. The __setitem__() method should only allow
#    existing records to be replaced; one easy way of doing this is to use the
#    __seek_to_index() method. With no state byte, __getitem__() is reduced to
#    a mere three lines. The __delitem__() method will need to be completely
#    rewritten since it must move all the records up to fill the gap; this can be
#    done in just over half a dozen lines, but does require some thought. The
#    undelete() method must be removed since it is not supported, and the compact()
#    and inplace_compact() methods must be removed because they are
#    no longer needed.
#    All told, the changes amount to fewer than 20 new or changed lines and
#    at least 60 deleted lines compared with the original, and not counting
#    doctests. A solution is provided in BinaryRecordFile_ans.py.

