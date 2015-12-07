from fabric.operations import run, sudo
from fabric.api import cd, env
from fabric.context_managers import nested, prefix
import os

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

HOME = os.getenv('HOME')

env.user = 'ubuntu'
env.hosts = [os.getenv('SERVER_IP')]
env.key_filename = ['{}/.ssh/{}.pem'.format(HOME, os.getenv('PEM'))]
env.sitedir = '/home/ubuntu/code/slack-fit/'
env.venv = 'slack-fit'
env.venv_activate = '. ~/.virtualenvs/{venv}/bin/activate'.format(**env)


def test_creds():
    run('echo "LOGGED IN"')


def restart_app():
    sudo('stop slackfit; true')
    sudo('rm -f /etc/init/slackfit.conf')
    sudo('etc/slackfit.conf /etc/init/slackfit.conf')
    sudo('service slackfit start')


def deploy():
    with nested(cd(env.sitedir), prefix(env.venv_activate)):
        run('git fetch')
        run('git reset --hard HEAD')
        run('git pull origin master')
        run('pip install --upgrade -r requirements.txt')
        restart_app()
