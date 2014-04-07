/*class disco {

    Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }


    exec { 'clone_disco':
        cwd => '/',
        command => "git clone git://github.com/discoproject/disco.git home/vagrant/src/disco",
        require => Package['git'],
    }

    exec { 'checkout_044':
        cwd => '/src/disco',
        command => "git checkout 0.4.4",
        require => Package['git'],
    }

    #exec { 'build_deb_files':
        #cwd => '/src/disco',
    #    command => "sh ./home/vagrante/src/disco/make-discoproject-debian",
    #}

}

include disco

*/