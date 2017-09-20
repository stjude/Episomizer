#!/usr/bin/env python3
"""
Python version: 3.6
Author: Liang Ding
Date: 9/20/2017
"""

import time


def timeit(method):
    """ Decorator to calculate elapse time.
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r %2.2f sec' % (method.__name__, te-ts))
        return result
    return timed
