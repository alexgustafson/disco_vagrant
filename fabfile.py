from fabric.api import env, local, run, cd, put, roles, sudo
from time import sleep

env.roledefs = {
    'master': ['192.168.50.4'],
    'nodes': ['192.168.50.10']
}

env.user = 'root'
env.password = "ska"
DISCO_REPO = 'https://github.com/discoproject/disco.git'
DISCO_REPO_BRANCH = 'master'
DISCO_RELATIVE_PATH = 'disco'
DISCO_ABSOLUTE_PATH = '/home/disco'

MASTER_TEMPLATE_FILES = 'templates/discomaster'
NODE01_TEMPLATE_FILES = 'templates/disconode1'


@roles('master', 'nodes')
def install_step_01():


    #setup ssh
    #run('echo root:ska | sudo chpasswd')
    try:
        run('mkdir -p /var/run/sshd')
    except:
        pass

    #passwordless login for root
    run("mkdir -p /root/.ssh")
    run("ssh-keygen -N '' -f /root/.ssh/id_dsa")
    run("cat /root/.ssh/id_dsa.pub >> /root/.ssh/authorized_keys")
    run('echo -n "localhost " > /root/.ssh/known_hosts')
    run('cat /etc/ssh/ssh_host_rsa_key.pub >> /root/.ssh/known_hosts')

    #passwordless login for disco
    run('adduser --system disco --shell /bin/sh')
    run('mkdir -p /home/disco/.ssh')
    run("ssh-keygen -N '' -f /home/disco/.ssh/id_dsa")
    run('cat /home/disco/.ssh/id_dsa.pub >> /home/disco/.ssh/authorized_keys')
    run('echo -n "localhost " > /home/disco/.ssh/known_hosts')
    run('cat /etc/ssh/ssh_host_rsa_key.pub >> /home/disco/.ssh/known_hosts')
    run('chown disco -R /home/disco/.ssh')


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
                run('git checkout tags/0.5')
                run('make')
                run('make install')
            except:
                pass
    else:
        #if we're on a node, do make install-node
        with cd(DISCO_RELATIVE_PATH):
            try:
                run('make')
                run('make install-node')
            except:
                pass

    run('chown -R disco /usr/local/var/disco')

    #add disco command line utility to system path
    '''
    print('add disco command line utility to system path')
    try:
        sudo('ln -s {0} /usr/local/bin'.format(DISCO_ABSOLUTE_PATH))
    except:
        pass
    '''

@roles('master', 'nodes')
def install_step_02():
    if env.host_string in env.roledefs['master']:
        #start disco quickly to generate the erlang cookie ( is this right? )
        with cd(DISCO_RELATIVE_PATH):
            run('bin/disco start')
            sleep(1)
            run('bin/disco stop')

        run('ssh disco@disconode1')
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
        run('bin/disco nodaemon') # TODO : once setup if correct change this to make disco a deamon

@roles('master')
def stop():
    with cd(DISCO_RELATIVE_PATH):
        run('bin/disco stop')
