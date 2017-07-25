#!/usr/bin/env python3

from fabric.api import run

def iso():
    run('date -u')
