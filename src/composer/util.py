#!/usr/bin/env python3
"""
Python version: 3.6

Author: Liang Ding
Date: 9/20/2017
"""

import time
import subprocess
import shlex


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


def run_shell_command_call(cmd):
    """ Wrapper of subprocess.check_call to take a cmd string as input
    Args:
        cmd (str): command to run
    """
    cmd_to_exec = shlex.split(cmd)
    subprocess.check_call(cmd_to_exec)
