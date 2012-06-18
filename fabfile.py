#!/usr/local/env python

from fabric.api import env, run, sudo
from fabric.operations import local, prompt
from fabric.context_managers import cd, prefix, settings

import os.path
import sys

VIRTUALENVDIR = '/usr/local/pythonenv'
VIRTUALENV = 'OSF'
ACTIVATE_SCRIPT = os.path.join (VIRTUALENVDIR, VIRTUALENV, 'bin/activate')
PROJECT = 'osf-2012'
DB_NAME = 'osf'
DB_USER_NAME = 'osf'
PROJECT_LOCATION = '/srv/django'
PROJECT_ROOT = os.path.join (PROJECT_LOCATION, PROJECT)
WSGI_FILE = 'osf/django.wsgi'
REPOSITORY = 'ssh://blueeyes.stuffed.animals/home/bjb/projects/osw/2012/web/osf'

def host_type ():
    run ('uname -a')


def wipe_code ():
    '''
    remove the code from the target machine
    '''
    with settings (warn_only = True):
        with cd (PROJECT_LOCATION):
            run ('rm -rf %s' % PROJECT)

def wipe_db ():
    '''
    remove all traces of the deployed database from the target machine
    '''
    with settings (warn_only = True):
        sudo ('dropdb %s' % DB_NAME, user='postgres')
        sudo ('dropuser %s' % DB_USER_NAME, user='postgres')

def wipe_virtualenv ():
    '''
    remove the virtualenv from the target machine
    '''
    with settings (warn_only = True):
        with cd (VIRTUALENVDIR):
            sudo ('rm -rf %s' % VIRTUALENV)

def wipe_all ():
    '''
    remove all traces of the deployment from the target machine
    '''
    wipe_code ()
    wipe_db ()
    wipe_virtualenv ()


def virtualenv ():
    '''
    install the virtualenv
    '''
    # virtualenv stuff
    with cd (VIRTUALENVDIR):
        sudo ('virtualenv --no-site-packages OSF')

    # 
    # when I upgrade puffin to squeeze, I can use this;
    # 

    # with prefix ('source %s' % ACTIVATE_SCRIPT):
    #     sudo ('easy_install pip')
    #     sudo ('pip install Django==1.4')
    #     sudo ('pip install South==1.4.2')
    #     sudo ('pip install psycopg2==2.4.5')
    #     sudo ('pip install ssh==1.7.14')
    #     sudo ('pip install yolk==0.4.3')

    #
    # in the meantime, I have to use this
    #

    with cd (VIRTUALENVDIR):
        sudo ('cp -r BYTEFLOW/bin/{easy,pip}* OSF/bin')
        sudo ('sed -i s/BYTEFLOW/OSF/ OSF/bin/pip')
        sudo ('sed -i s/BYTEFLOW/OSF/ OSF/bin/pip-2.5')
        sudo ('sed -i s/BYTEFLOW/OSF/ OSF/bin/easy_install')
        sudo ('sed -i s/BYTEFLOW/OSF/ OSF/bin/easy_install-2.5')
        sudo ('cp -r BYTEFLOW/lib/python2.5/site-packages/{easy-install.pth,pip-0.8-py2.5.egg,setuptools-0.6c8-py2.5.egg,setuptools.pth} OSF/lib/python2.5/site-packages')

    with prefix ('source %s' % ACTIVATE_SCRIPT):
        sudo ('pip install Django==1.4')
        sudo ('pip install South==0.7.5')
        sudo ('pip install psycopg2==2.4.5')
        sudo ('pip install ssh==1.7.14')
        sudo ('pip install yolk==0.4.3')

    #
    # end of workaround for lenny/squeeze
    #


def db ():
    '''
    create the db and db owner
    '''
    # db stuff:  user and db
    DB_USER_PASSWORD = prompt ('password for new db user %s?' % DB_USER_NAME)
    sudo ('createuser -S -R -D %s' % DB_USER_NAME, user='postgres')
    run ('echo "ALTER USER %s PASSWORD \'%s\'" | sudo -u postgres psql %s' % (DB_USER_NAME, DB_USER_PASSWORD, 'template1'))
    sudo ('createdb -O %s %s' % (DB_USER_NAME, DB_NAME), user='postgres')

    sys.stdout.write ('WARNING!  still need to integrate into apache configs\n')
    sys.stdout.write ('WARNING!  do I need to adjust file perms after pip install?')


def restart ():
    '''
    restart postgresql and apache2
    '''
    # project code deployment stuff
    with prefix ('source %s' % ACTIVATE_SCRIPT):
        sudo ('invoke-rc.d postgresql-8.3 stop')
        sudo ('invoke-rc.d postgresql-8.3 start')
        # actually this doesn't really go here ... 
        # apache config fragment comes with actual source code
        # hmm.
        sudo ('invoke-rc.d apache2 stop')
        sudo ('invoke-rc.d apache2 start')




def new_deployment ():
    '''
    set up new machine for this website (db&user, virtualenv, code)

    assume postgres and apache are already installed
    '''
    virtualenv ()
    db ()
    restart ()


def restart_app ():
    with cd (PROJECT_ROOT):
        with prefix ('source %s' % ACTIVATE_SCRIPT):
            run ('touch %s' % os.path.join (PROJECT_ROOT, WSGI_FILE))

def deploy_version (version_id):
    '''
    checkout and deploy version_id of the software
    '''
    local ('git checkout %s' % version_id)

    with cd (PROJECT_LOCATION):
        run ('rm -rf %s' % PROJECT)
        run ('git archive --format=tar --remote=%s --prefix=%s/ %s | tar -xf -' % (REPOSITORY, PROJECT, version_id))

    with cd (PROJECT_ROOT):
        with prefix ('source %s' % ACTIVATE_SCRIPT):
            sudo ('chown bjb.www-data static')
            sudo ('chmod 2775 static')
            run ('./manage.py syncdb --settings=osf.settings')
            run ('./manage.py migrate --settings=osf.settings')
            run ('./manage.py collectstatic --settings=osf.settings')
            run ('./manage.py compilemessages --settings=osf.settings')
            sudo ('chown bjb.www-data osf/log')
            sudo ('chmod 2775 osf/log')
            sudo ('touch osf/log/error.log')
            sudo ('chown bjb.www-data osf/log/error.log')
            sudo ('chmod 775 osf/log/error.log')

    restart_app ()

    ## if the apache config fragment changed, do this
    # sudo ('invoke-rc.d apache2 stop')
    # sudo ('invoke-rc.d apache2 start')


    sys.stdout.write ('Are file ownerships correct?  Are permissions correct?\n')

