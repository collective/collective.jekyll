#!/usr/bin/make
#
pybot_options =

.PHONY: instance cleanall test robot stop

PACKAGE_ROOT = src/collective/jekyll

GS_FILES = $(PACKAGE_ROOT)/profiles/*/*.xml $(PACKAGE_ROOT)/setuphandlers.py

BUILDOUT_FILES = buildout.cfg setup.py bin/buildout dev.cfg pybot.cfg

DATA_FS = var/filestorage/Data.fs

all: instance

ifneq ($(strip $(TRAVIS)),)
IS_TRAVIS = yes
endif

ifdef IS_TRAVIS

# use cache to accelerate download 
plone-download-cache-4.1.4.tgz:
	wget https://github.com/downloads/plone/Products.CMFPlone/download-and-eggs-plone-4.1.4.tgz
 
download-cache: download-and-eggs-plone-4.1.4.tgz
	tar -xzf download-and-eggs-plone-4.1.4.tgz

instance_options = -ov

# use specific buildout that depends on cache
buildout.cfg: travis.cfg download-cache
	ln -s travis.cfg buildout.cfg

# use python as Travis has setup the virtualenv
develop-eggs: bootstrap.py buildout.cfg
	python bootstrap.py

else

# make a virtualenv
bin/python:
	virtualenv-2.6 --no-site-packages .

instance_options = -Nvt 5

buildout.cfg:
	ln -s dev.cfg buildout.cfg

develop-eggs: bin/python bootstrap.py buildout.cfg
	./bin/python bootstrap.py

endif

bin/buildout: develop-eggs

bin/test: $(BUILDOUT_FILES)
	./bin/buildout -Nvt 5 install test
	touch $@

parts/instance: $(BUILDOUT_FILES)
	./bin/buildout $(instance_options) install instance

bin/instance: parts/instance
	touch $@
	
var/plonesite: $(GS_FILES) bin/instance
	if [ -f var/supervisord.pid ]; then bin/supervisorctl shutdown; sleep 5; fi
	./bin/buildout -Nvt 5 install plonesite
	touch $@

instance: var/plonesite
	bin/instance fg

cleanall:
	rm -fr bin develop-eggs downloads eggs parts .installed.cfg

test: bin/test	
	./bin/test

bin/pybot: $(BUILDOUT_FILES)
	./bin/buildout -Nvt 5 install robot
	touch $@

bin/supervisord: $(BUILDOUT_FILES)
	./bin/buildout -Nvt 5 install varnish-build varnish-conf varnish supervisor
	touch $@

bin/supervisorctl: bin/supervisord
	touch $@

var/supervisord.pid: bin/supervisord bin/instance bin/supervisorctl
	if [ -f var/supervisord.pid ]; then bin/supervisorctl shutdown; sleep 5; fi
	bin/supervisord --pidfile=$@
	bin/supervisorctl start all
	touch $@

robot: bin/pybot var/plonesite var/supervisord.pid
	bin/pybot $(pybot_options) -d robot-output acceptance-tests

stop: 
	bin/supervisorctl shutdown
