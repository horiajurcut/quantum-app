#!/bin/bash
(
	touch /home/vagrant/.nano_history

	export DEBIAN_FRONTEND=noninteractive

	echo ""
	echo "### Fixing dns entries"
	sed -i -e"s/domain-name-servers, //g" /etc/dhcp/dhclient.conf
	if [ -z "`grep -Fl 'prepend domain-name-servers 8.8.8.8,8.8.4.4;' /etc/dhcp/dhclient.conf`" ]; then
		echo $'\n'"prepend domain-name-servers 8.8.8.8,8.8.4.4;" >> /etc/dhcp/dhclient.conf
	fi
	(dhclient -r && dhclient eth0)

	locale-gen UTF-8

	echo ""
	echo "### Add color prompt"
	touch /home/vagrant/.nano_history
	chown vagrant:vagrant /home/vagrant/.nano_history
	sed -i -e"s/#force_color_prompt=yes/force_color_prompt=yes/g" /home/vagrant/.bashrc
	source /home/vagrant/.bashrc

	echo ""
	echo "### Updating apt data"
	apt-get update

	# echo "### Installing necessary packages"
	# apt-get -q -y install \
	# 	htop git git-flow nodejs php5-cli php5-curl \
	# 	redis-server \
	# 	mysql-server-5.5 mysql-client-5.5 libmysqlclient-dev \
	# 	ruby1.9.1-dev

	echo "### Installing necessary packages"
	apt-get -q -y install \
		htop git git-flow \
		python-setuptools \
		mysql-server-5.5 mysql-client-5.5 libmysqlclient-dev \
		build-essential python-dev libmysqlclient-dev


	echo ""
	echo "### Configure MySQL for remote connections"
	sed -i -e"s/bind-address/#bind-address/g" /etc/mysql/my.cnf
	mysql -uroot -e"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;"
	service mysql restart

	# echo ""
	# echo "### Start Redis"
	# redis-server &

	echo ""
	echo "### Install Celery"
	sudo easy_install pip

	echo ""
	echo "### Cleanup packages"
	apt-get -q -y autoremove

	echo ""
	echo "### Change default editor to vim"
	if [ -z "`grep -Fl 'EDITOR=vim' /home/vagrant/.bashrc`" ]; then
		echo $'\n''export EDITOR=vim' >> /home/vagrant/.bashrc
		source /home/vagrant/.bashrc
	fi

	echo ""
	echo "### Bootstrap completed"

)
#2>&1 | logger -t vagrant.bootstrap
exit 0
