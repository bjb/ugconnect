#!/usr/local/env python

from fabric.api import run

def host_type ():
    run ('uname -a')

