from fabric.api import env, local, run, cd, put, roles, sudo
from time import sleep

env.roledefs = {
    'master': ['192.168.50.4'],
    'nodes':  ['192.168.50.10']
}

DISCO_REPO = 'https://github.com/discoproject/disco.git'
DISCO_REPO_BRANCH = 'master'
DISCO_RELATIVE_PATH = 'disco'
DISCO_HOME = '/home/vagrant/disco'
DISCO_MASTER_HOST = 'discomaster'
DISCO_PORT = 8989

MASTER_TEMPLATE_FILES = 'templates/discomaster'
NODE01_TEMPLATE_FILES = 'templates/disconode1'

# script asks for vagrant password - it is 'vagrant'
# keep in mind that the default user is vagrant within this script

env.no keys = True # discourages use of $HOME/.ssh/ key files
env.user = 'vagrant' # This is the default username anyway

@roles('master', 'nodes')
def install_step_01():
 
  #create keys for vagrant user
  run("ssh-keygen -t ecdsa -N '' -f /home/vagrant/.ssh/id_ecdsa")

  #copy over custom hosts file so that we dont have to mess with any DNS
  print('copying hosts file to /etc/hosts')
  if env.host_string in env.roledefs['master']:
    put('{0}/hosts'.format(MASTER_TEMPLATE_FILES), "/etc/hosts", use_sudo=True)
  elif env.host_string in env.roledefs['nodes']:
    put('{0}/hosts'.format(NODE01_TEMPLATE_FILES), "/etc/hosts", use_sudo=True)

@roles('master', 'nodes')
def install_step_02():

# copy the public keys in one system to the other system
  if env.host_string in env.roledefs['master']
    run("ssh-copy-id -i ~/.ssh/id_ecdsa.pub vagrant@disconode1")
  else
    run("ssh-copy-id -i ~/.ssh/id_ecdsa.pub vagrant@discomaster")
    
@roles('master', 'nodes')
def install_step_03():

  run("mkdir -p {0}".format(DISCO_HOME))
  
  #clone the disco repository
  print('clone disco repo from github')
  try:
    run('git clone {0} {1}'.format(DISCO_REPO, DISCO_HOME))
  except:
    pass

  if env.host_string in env.roledefs['master']:
    #if we're on the master node, do normal make install
    with cd(DISCO_HOME):
      try:
        run('git checkout tags/0.5')
        run('make')
        run('sudo make install')
      except:
        pass
  else:
    #if we're on a node, do make install-node
    with cd(DISCO_HOME):
      try:
        run('make')
        run('sudo make install-node')
        print('add disco command line utilities to system path')
        try:
          sudo('ln -s {0}/bin/disco /usr/local/bin'.format(DISCO_HOME))
          sudo('ln -s {0}/bin/ddfs  /usr/local/bin'.format(DISCO_HOME))
        except:
          pass
      except:
        pass

  run('sudo chown -R vagrant:vagrant /usr/local/bin')
  run('sudo chown -R vagrant:vagrant /usr/local/var')

@roles('master', 'nodes')
def install_step_04():
  if env.host_string in env.roledefs['master']:
    #start disco quickly to generate the erlang cookie ( is this right? )
    with cd(DISCO_HOME):
      run('bin/disco start')
      sleep(1)
      run('bin/disco stop')
      # copy discomaster .erlang.cookie to disconode1
      try:
        run("scp /home/vagrant/.erlang.cookie vagrant@disconode1:/home/vagrant")
      except:
        pass

@roles('master')
def start():
  with cd(DISCO_HOME):
    run('bin/disco nodaemon') # TODO : once setup if correct change this to make disco a deamon

@roles('master')
def stop():
  with cd(DISCO_HOME):
    run('bin/disco stop')
