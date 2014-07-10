# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise64"

	config.vm.network :forwarded_port, guest: 8080, host: 8081, auto_correct: true
	config.vm.network :forwarded_port, guest: 5000, host: 5000, auto_correct: true
	config.vm.network :forwarded_port, guest: 5432, host: 5432, auto_correct: true
	config.vm.network :forwarded_port, guest: 8888, host: 8889, auto_correct: true
	config.vm.network :forwarded_port, guest: 80, host: 8088, auto_correct: true

	# Create a private network, which allows host-only access to the machine
	# using a specific IP.
	config.vm.network :public_network

end
