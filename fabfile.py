from fabric.api import env, local, run, cd, put, roles, sudo
from time import sleep

env.roledefs = {
    'master': ['192.168.50.4'],
    'nodes': ['192.168.50.10']
}

env.user = 'vagrant'
env.password = "vagrant"
DISCO_REPO = 'https://github.com/discoproject/disco.git'
DISCO_REPO_BRANCH = 'master'
DISCO_RELATIVE_PATH = 'disco'
DISCO_ABSOLUTE_PATH = '/home/vagrant/disco'

MASTER_TEMPLATE_FILES = 'templates/discomaster'
NODE01_TEMPLATE_FILES = 'templates/disconode1'


@roles('master', 'nodes')
def install_step_01():

    #copy over custom hosts file so that we dont have to mess with any DNS
    print('copying hosts file to /etc/hosts')
    if env.host_string in env.roledefs['master']:
        put('{0}/hosts'.format(MASTER_TEMPLATE_FILES), "/etc/hosts", use_sudo=True)
    elif env.host_string in env.roledefs['nodes']:
        put('{0}/hosts'.format(NODE01_TEMPLATE_FILES), "/etc/hosts", use_sudo=True)


    #clone the disco repository
    print('clone disco repo from github')
    try:
        run('git clone {0} {1}'.format(DISCO_REPO, DISCO_RELATIVE_PATH))
    except:
        pass

    if env.host_string in env.roledefs['master']:
        #if we're on the master node, do normal make install
        with cd(DISCO_RELATIVE_PATH):
            try:
                sudo('make install')
            except:
                pass
    else:
        #if we're on a node, do make install-node
        with cd(DISCO_RELATIVE_PATH):
            try:
                sudo('make install-node')
            except:
                pass

    #add disco command line utility to system path
    print('add disco command line utility to system path')
    try:
        sudo('ln -s {0} /usr/local/bin'.format(DISCO_ABSOLUTE_PATH))
    except:
        pass

@roles('master', 'nodes')
def install_step_02():
    if env.host_string in env.roledefs['master']:
        #start disco quickly to generate the erlang cookie ( is this right? )
        with cd(DISCO_RELATIVE_PATH):
            sudo('bin/disco start')
            sleep(1)
            sudo('bin/disco stop')

        run('ssh vagrant@disconode1')
        try:
            run("ssh-keygen -N '' -f ~/.ssh/id_dsa")
            run("ssh-copy-id disconode1")
        except:
            pass

        try:
            run("scp ~/.erlang.cookie disconode1")
        except:
            pass

@roles('master')
def start():
    with cd(DISCO_RELATIVE_PATH):
        sudo('bin/disco nodaemon') # TODO : once setup if correct change this to make disco a deamon

@roles('master')
def stop():
    with cd(DISCO_RELATIVE_PATH):
        sudo('bin/disco stop')