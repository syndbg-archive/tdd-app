import random

from fabric.api import env, local, run, cd, sudo
from fabric.contrib.files import append, exists, sed


REPO_URL = 'git@github.com:HackBulgaria/Odin.git'


def provision():
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host)
    _create_directory_structure_if_neccessary(site_folder)
    _install_requirements_if_neccessary()


def _install_requirements_if_neccessary():
    sudo('apt-get update')
    sudo('apt-get install nginx, python3-pip, python-pip')
    sudo('pip3 install virtualenv')


def deploy():
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host)
    source_folder = site_folder + '/source'

    _create_directory_structure_if_neccessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _create_or_update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_neccessary(site_folder):
    subfolders_to_create = ('database', 'source', 'static', 'virtualenv')
    for subfolder in subfolders_to_create:
        run('mkdir -p {}/{}'.format(site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        with cd(source_folder):
            run('git fetch')
    else:
        run('git clone {} {}'.format(REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    with cd(source_folder):
        run('git reset --hard {}'.format(current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', "DEBUG = False")
    sed(settings_path, 'ALLOWED_HOSTS =.+S', 'ALLOWED_HOSTS = ["{}"]'.format(site_name))

    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _create_or_update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder, '/bin/pip'):
        run('virtualenv --python=python3 {}'.format(virtualenv_folder))
    run('{}/bin/pip install -r {}/requirements.pip'.format(virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    with cd(source_folder):
        run('../virtualenv/bin/python3 manage.py collectstatic --noinput')


def _update_database(source_folder):
    with cd(source_folder):
        run('../virtualenv/bin/python3 manage.py migrate --noinput')
