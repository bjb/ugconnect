#!/usr/local/env python

from fabric.api import run

def host_type ():
    run ('uname -a')



def push_version (xxx):
    '''
    push version xxx to the server
    '''
    sys.stdout.write ('push_version:  NIY')

def use_version (xxx):
    '''
    checkout version xxx
    ./manage.py syncdb
    ./manage.py south migrate
    ./manage.py makemessages (internationalization stuff)
    restart web server
    '''
    sys.stdout.write ('use_version:  NIY')



# assumes postgres and apache are already installed
def new_deployment ():
    '''
    createuser and createdb on postgres
    create/install an apache config  (file to be included into a virtualhost)
    git clone the software on the server
    '''
    sys.stdout.write ('new_deployment:  NIY')


def deploy_new_version (xxx):
    '''
    call push_version (xxx)
    call use_version (xxx)
    '''
    sys.stdout.write ('deploy_new_version:  NIY')


def revert_to_version (old_version):
    '''
    call use_version (old_version)
    '''
    sys.stdout.write ('revert_to_version:  NIY')
