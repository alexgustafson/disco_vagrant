# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.provision "shell", inline:
    "echo discomaster setup"

    config.vm.define "disco_master" do |master|

        # Every Vagrant virtual environment requires a box to build off of.
        config.vm.box = "discomaster"

        # The url from where the 'config.vm.box' box will be fetched if it
        # doesn't already exist on the user's system.
        config.vm.box_url = "http://files.vagrantup.com/lucid64.box"

        # Create a private network, which allows host-only access to the machine
        # using a specific IP.
        master.vm.network "private_network", ip: "192.168.50.4"

        # If true, then any SSH connections made will enable agent forwarding.
        # Default value: false
        config.ssh.forward_agent = true

        # Share an additional folder to the guest VM. The first argument is
        # the path on the host to the actual folder. The second argument is
        # the path on the guest to mount the folder. And the optional third
        # argument is a set of non-required options.
        master.vm.synced_folder "shared_folders/discomaster/data", "/vagrant_data"

        master.vm.hostname = "discomaster"
        master.ssh.guest_port = 22

        master.vm.provision :puppet do |puppet|
            puppet.manifests_path = "puppetfiles/manifests"
            puppet.manifest_file  = "init.pp"
            puppet.module_path = "puppetfiles/modules"
            puppet.options = "--verbose --debug"
        end
    end

    "echo disco_node setup"

    config.vm.define "disconode1" do |node01|

        node01.vm.box = "disconode1"
        config.vm.box_url = "http://files.vagrantup.com/lucid64.box"
        node01.vm.network "private_network", ip: "192.168.50.10"
        node01.vm.synced_folder "shared_folders/disconode1/data", "/vagrant_data"
        node01.vm.hostname = "disconode1"

        node01.ssh.guest_port = 22

        node01.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
        end

        node01.vm.provision :puppet do |puppet|
            puppet.manifests_path = "puppetfiles/manifests"
            puppet.manifest_file  = "init.pp"
            puppet.module_path = "puppetfiles/modules"
            puppet.options = "--verbose --debug"
        end

    end
end
