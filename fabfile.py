from fabric.api import env, local, run, cd, put, roles

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

    #make disco
    print('make disco')
    with cd(DISCO_RELATIVE_PATH):
        try:
            run('make')
        except:
            pass

    if env.host_string in env.roledefs['master']:
        with cd(DISCO_RELATIVE_PATH):
            try:
                run('make install')
            except:
                pass
    else:
        with cd(DISCO_RELATIVE_PATH):
            try:
                run('make install-node')
            except:
                pass

    #add disco command line utility to system path
    print('add disco command line utility to system path')
    try:
        run('ln -s {0} /usr/local/bin'.format(DISCO_ABSOLUTE_PATH))
    except:
        pass

@roles('master', 'nodes')
def install_step_02():
    if env.host_string in env.roledefs['master']:
        run("ssh-keygen -N '' -f ~/.ssh/id_dsa")
        run("ssh-copy-id disconode1")
        run("scp ~/.erlang.cookie disconode1y")

@roles('master')
def start():
    with cd(DISCO_RELATIVE_PATH):
        run('bin/disco nodaemon') # TODO : once setup if finished change this to make disco a deamon

@roles('master')
def stop():
    with cd(DISCO_RELATIVE_PATH):
        run('bin/disco stop')