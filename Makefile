#!/usr/bin/make
#
options =

.PHONY: instance cleanall test robot

PACKAGE_ROOT = src/collective/jekyll

GS_FILES = $(PACKAGE_ROOT)/profiles/*/*.xml $(PACKAGE_ROOT)/setuphandlers.py

BUILDOUT_FILES = buildout.cfg setup.py bin/buildout

PYBOT_BUILDOUT_FILES = $(BUILDOUT_FILES) pybot.cfg

DATA_FS = var/filestorage/Data.fs

all: instance

ifneq ($(strip $(TRAVIS_PYTHON_VERSION)),)
IS_TRAVIS = yes
endif

ifdef IS_TRAVIS
buildout-cache:
	wget https://github.com/downloads/plone/Products.CMFPlone/plone-buildout-cache-4.1.4.tgz
	tar -xzf plone-buildout-cache-4.1.4.tgz

develop-eggs: bootstrap.py buildout.cfg
	python bootstrap.py

buildout.cfg:
	ln -s travis.cfg buildout.cfg

else
bin/python:
	virtualenv-2.6 --no-site-packages .

develop-eggs: bin/python bootstrap.py buildout.cfg
	./bin/python bootstrap.py

buildout.cfg:
	ln -s dev.cfg buildout.cfg

endif

bin/buildout: develop-eggs

bin/test: $(BUILDOUT_FILES)
	./bin/buildout -Nvt 5 install test
	touch $@

bin/instance: $(BUILDOUT_FILES)
	./bin/buildout -Nvt 5 install instance
	touch $@
	
$(DATA_FS): $(GS_FILES)	bin/instance
	if [ -f var/supervisord.pid ]; then bin/supervisorctl shutdown; sleep 5; fi
	./bin/buildout -Nvt 5 install plonesite

instance: bin/instance $(DATA_FS)
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

robot: bin/pybot var/supervisord.pid
	bin/pybot $(options) -d robot-output acceptance-tests
