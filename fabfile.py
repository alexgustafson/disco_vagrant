from fabric.api import env, local, run, cd, put

def disco_master():
    env.user = 'vagrant'
    env.hosts = ["vagrant@192.168.50.4"]
    env.password = "vagrant"
    env.disco_repo = 'https://github.com/discoproject/disco.git'
    env.disco_repo_branch = 'master'
    env.disco_path = 'disco'
    env.disco_absolute_path = '/home/vagrant/disco'
    env.local_files = 'templates/discomaster'
    env.master = True


def disco_node_1():
    env.user = 'vagrant'
    env.hosts = ["vagrant@192.168.50.10"]
    env.password = "vagrant"
    env.disco_repo = 'https://github.com/discoproject/disco.git'
    env.disco_repo_branch = 'master'
    env.disco_path = 'disco'
    env.disco_absolute_path = '/home/vagrant/disco'
    env.local_files = 'templates/disconode1'
    env.master = False


def initialize():
    #switch to master
    print('** switching to discomaster **')
    disco_master()

    #do install step 1 on master
    try:
        print('** initial install step 1 on discomaster **')
        install_step_01()
    except Exception, e:
        pass

    #switch to disconode1
    print('** switching to disconode1 **')
    disco_node_1()

    #do install step 1 on disconode1
    try:
        print('** initial install step 1 on disconode1 **')
        install_step_01()
    except Exception, e:
        pass

    #switch to master
    print('** switching to discomaster **')
    disco_master()
    try:
        print('** initial install step 2 on discomaster **')
        install_step_02()
    except Exception, e:
        pass


def install_step_01():
    #copy over custom hosts file so that we dont have to mess with any DNS
    print('copying hosts file to /etc/hosts')
    put('{0}/hosts'.format(env.local_files), "/etc/hosts", use_sudo=True)

    #clone the disco repository
    print('clone disco repo from github')
    run('git clone {0} {1}'.format(env.disco_repo, env.disco_path))

    #make disco
    print('make disco')
    with cd(env.disco_path):
        run('make')

    #add disco command line utility to system path
    print('add disco command line utility to system path')
    run('ln -s {0} /usr/local/bin'.format(env.disco_absolute_path))


def install_step_02():
    if env.master:
        run("ssh-keygen -N '' -f ~/.ssh/id_dsa")
        run("ssh-copy-id disconode1")
        run("scp ~/.erlang.cookie disconode1:")


def start():
    with cd(env.disco_path):
        run('bin/disco nodaemon') # TODO : once setup if finished change this to make disco a deamon


def stop():
    with cd(env.disco_path):
        run('bin/disco stop')