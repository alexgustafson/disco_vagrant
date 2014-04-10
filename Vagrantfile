# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.provision "shell", inline: "echo discomaster setup"

    config.vm.define "discomaster" do |discomaster|

        # Every Vagrant virtual environment requires a box to build off of.
        discomaster.vm.box = "disco_box"

        # The url from where the 'config.vm.box' box will be fetched if it
        # doesn't already exist on the user's system.
        discomaster.vm.box_url = "http://puppet-vagrant-boxes.puppetlabs.com/ubuntu-1310-i386-virtualbox-puppet.box"

        # Create a private network, which allows host-only access to the machine
        # using a specific IP.
        discomaster.vm.network "private_network", ip: "192.168.50.4"

        # If true, then any SSH connections made will enable agent forwarding.
        # Default value: false
        discomaster.ssh.forward_agent = true

        # Share an additional folder to the guest VM. The first argument is
        # the path on the host to the actual folder. The second argument is
        # the path on the guest to mount the folder. And the optional third
        # argument is a set of non-required options.
        discomaster.vm.synced_folder "shared_folders/discomaster/data", "/vagrant_data"

        discomaster.vm.hostname = "discomaster"
        discomaster.ssh.guest_port = 22

        discomaster.vm.provision :puppet do |puppet|
     		puppet.manifests_path = "puppetfiles/manifests"
     		puppet.manifest_file  = "init.pp"
     		puppet.options = "--verbose --debug"
   	    end

    end

    config.vm.define "disconode1" do |disconode1|

        disconode1.vm.box = "disco_box"
        disconode1.vm.box_url = "http://puppet-vagrant-boxes.puppetlabs.com/ubuntu-1310-i386-virtualbox-puppet.box"
        disconode1.vm.network "private_network", ip: "192.168.50.10"
        disconode1.vm.synced_folder "shared_folders/disconode1/data", "/vagrant_data"
        disconode1.vm.hostname = "disconode1"

        disconode1.ssh.guest_port = 22

        disconode1.vm.provision :puppet do |puppet|
     		puppet.manifests_path = "puppetfiles/manifests"
     		puppet.manifest_file  = "init.pp"
     		puppet.options = "--verbose --debug"
   	    end

    end
end
