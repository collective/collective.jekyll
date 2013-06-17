#!/usr/bin/make
#
pybot_options =

.PHONY: instance cleanall test robot stop

PACKAGE_ROOT = src/collective/jekyll

GS_FILES = $(PACKAGE_ROOT)/profiles/*/*.xml $(PACKAGE_ROOT)/setuphandlers.py

BUILDOUT_COMMAND = ./bin/buildout -Nt 5

all: instance

BUILDOUT_FILES = buildout.cfg buildout-varnish.cfg setup.py bin/buildout

ifneq ($(strip $(TRAVIS)),)
IS_TRAVIS = yes
endif

ifdef IS_TRAVIS

# use specific buildout that depends on cache
buildout.cfg: travis.cfg
	cp travis.cfg buildout.cfg

# use python as Travis has setup the virtualenv
bin/buildout: bootstrap.py buildout.cfg
  mkdir -p buildout-cache/downloads
	python bootstrap.py
	touch $@

else

# make a virtualenv
bin/python:
	virtualenv-2.7 --no-site-packages .
	touch $@

buildout.cfg:
	cp dev.cfg buildout.cfg

bin/buildout: bin/python bootstrap.py buildout.cfg
	./bin/python bootstrap.py
	touch $@

endif

bin/test: $(BUILDOUT_FILES) bin/supervisord
	$(BUILDOUT_COMMAND) install test test-wrap-varnish
	touch $@

parts/instance: $(BUILDOUT_FILES)
	$(BUILDOUT_COMMAND) install instance
	touch $@

bin/instance: parts/instance
	if [ -f var/plonesite ]; then rm var/plonesite; fi
	touch $@
	
var/plonesite: $(GS_FILES) bin/instance
	$(BUILDOUT_COMMAND) install plonesite
	touch $@

instance: var/plonesite
	bin/instance fg

cleanall:
	if [ -f var/supervisord.pid ]; then bin/supervisorctl shutdown; sleep 5; fi
	rm -fr bin develop-eggs downloads eggs parts .installed.cfg

test: bin/test	
	./bin/test

bin/robot: $(BUILDOUT_FILES)
	$(BUILDOUT_COMMAND) install robot
	touch $@

bin/supervisord: $(BUILDOUT_FILES)
	$(BUILDOUT_COMMAND) install varnish-build varnish-conf varnish supervisor
	touch $@

bin/supervisorctl: bin/supervisord
	touch $@

var/supervisord.pid: bin/supervisord bin/supervisorctl
	if [ -f var/supervisord.pid ]; then bin/supervisorctl shutdown; sleep 5; fi
	bin/supervisord --pidfile=$@

robot: bin/pybot var/supervisord.pid
	bin/robot $(pybot_options) -d robot-output

stop: 
	bin/supervisorctl shutdown
