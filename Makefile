#!/usr/bin/make
#
options =

.PHONY: instance cleanall test robot stop

PACKAGE_ROOT = src/collective/jekyll

GS_FILES = $(PACKAGE_ROOT)/profiles/*/*.xml $(PACKAGE_ROOT)/setuphandlers.py

BUILDOUT_FILES = buildout.cfg setup.py bin/buildout

PYBOT_BUILDOUT_FILES = $(BUILDOUT_FILES) pybot.cfg

DATA_FS = var/filestorage/Data.fs

all: instance

ifneq ($(strip $(TRAVIS)),)
IS_TRAVIS = yes
endif

ifdef IS_TRAVIS

# use cache to accelerate download 
plone-download-cache-4.1.4.tgz:
	wget https://github.com/downloads/plone/Products.CMFPlone/plone-download
 
download-cache: plone-download-cache-4.1.4.tgz
	tar -xzf plone-download-cache-4.1.4.tgz

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

buildout.cfg:
	ln -s dev.cfg buildout.cfg

develop-eggs: bin/python bootstrap.py buildout.cfg
	./bin/python bootstrap.py

endif

bin/buildout: develop-eggs

bin/test: $(BUILDOUT_FILES)
	./bin/buildout -Nvt 5 install test
	touch $@

bin/instance: $(BUILDOUT_FILES)
	./bin/buildout -Nvt 5 install instance
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

bin/pybot: $(PYBOT_BUILDOUT_FILES)
	./bin/buildout -Nvt 5 -c pybot.cfg install robot
	touch $@

bin/supervisord: $(PYBOT_BUILDOUT_FILES)
	./bin/buildout -Nvt 5 -c pybot.cfg install supervisor
	touch $@

bin/supervisorctl: bin/supervisord
	touch $@

var/supervisord.pid: bin/supervisord bin/instance bin/supervisorctl
	if [ -f var/supervisord.pid ]; then bin/supervisorctl shutdown; sleep 5; fi
	bin/supervisord --pidfile=$@
	bin/supervisorctl start all
	touch $@

robot: bin/pybot var/plonesite var/supervisord.pid
	bin/pybot $(options) -d robot-output acceptance-tests

stop: 
	bin/supervisorctl shutdown
