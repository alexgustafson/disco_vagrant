Disco on Vagrant
================

Dependencies:

    VirtualBox
    Vagrant
    Fabric
    
    you need to have Vagrant installed on your system. Get a newer version from the
    Vagrant website http://vagrantup.com The older gem packages are not compatible
    
    The Vagrant boxes will only be able to run on a host that has VirtualBox installed.
    
    you need to have Fabric installed in your python environment.
    If you don't want to install fabric in your system library then
    create a python virtual envelope and install from the requirements
    file.
    
    for example:
    
    >> cd disco_vagrant
    >> virtualenv env
    >> pip install -r requirements.txt
    >> source env/bin/active
    
    your open terminal will now be running with the necessary python
    extensions.


Setup and Installation:

    clone this repository
    
        >> git clone https://github.com/alexgustafson/disco_vagrant.git
    
    cd into disco_vagrant
    
        >> cd disco_vagrant
    
    build the vagrant vms for discomaster and disconode1
    
        if you have previously built virtual boxes running, you may want
        to 'vagrant destroy'
        before making new virtual boxes in this next step
    
        >> vagrant up
    
        this will take a while, vagrant needs to download the basic box and
        configure the 2 vagrant environments. After this command the 2 vagrant
        boxes will be running in the background.
        
        test by doing 'vagrant ssh discomaster' and then 'exit'
        *** See also 'SanityTests.txt' document for state at this point ***
    
    generate the ssh key, copy the key from discomaster to disconode1
    
        if any of these steps hang and fail, just do it over again..
        keep your eyes open - password 'vagrant' required and 'yes' required occasionally.
    
        >> fab install_step_01
        
        >> fab install_step_02
        
    clone and make disco on the master and node
 
        >> fab install_step_03
        
    generate the erlang cookie and copy to disconode1
        
        >> fab install_step_04
        
    should be runnable
        
        >> fab start
        
    stop disco when you are finished
        
        >> fab stop

Better test with results given in 'FinalTest.txt' document

