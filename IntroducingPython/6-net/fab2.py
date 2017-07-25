#!/usr/bin/env python3

from fabric.api import local

def iso():
    local('date -u')
