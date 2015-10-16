## Linux Ramdump Parser for Windows ##

#### Require: ####
[Python / Cygwin](https://cygwin.com/)

#### Useage: ####
	git clone https://github.com/kiddlu/ramparser.git /usr/lib/ramparser
	python /usr/lib/ramparser/pyelftools/setup.py install
	ln -s /usr/lib/ramparser/ramparser.sh /usr/bin/ramparser

	cd /ramdump_vmlinux_dir/
	ramparser