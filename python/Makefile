export CXX
export CC

## Work out the platform for python wheels
PLATFORM := $(shell uname -s)
ifeq ($(filter Linux Windows Darwin,$(PLATFORM)),)
PLATFORM := Windows
endif
PLATFORM := $(shell echo $(PLATFORM) | tr '[:upper:]' '[:lower:]')
#PLATFORM :="$(PLATFORM)-$(shell arch)"
all : wheels

ifeq ($(PLATFORM),windows)
wheels :
	cmd /c build-all-wheels.bat
else
SHELL := bash
wheels :
	bash build-all-wheels.sh
sdist :
	python2 setup.py sdist
	python3 setup.py sdist
	
endif


clean :
	rm -rf build
	rm -rf dist

upload :
	find dist -type f -print | while IFS= read -r f; do \
		twine upload $$f; \
	done

install :
	if (which pip2); then pip2 install uWebSockets --no-index -f dist; fi
	if (which pip3); then pip3 install uWebSockets --no-index -f dist; fi
	if [[ -d /opt/python/*/bin ]]; then \
		for PYBIN in /opt/python/*/bin; do \
			"$${PYBIN}/pip" install uWebSockets --no-index -f dist; \
		done; \
	fi
	
uninstall :
	pip2 uninstall -y uWebSockets
	pip3 uninstall -y uWebSockets
	if [[ -d /opt/python/*/bin ]]; then \
		for PYBIN in /opt/python/*/bin; do \
			"$${PYBIN}/pip" uninstall -y uWebSockets --no-index -f dist; \
		done; \
	fi
	

## Wrappers for building with Vagrant/Docker
VAGRANT_PROVIDER ?= docker
VAGRANT_HOST ?= manylinux
.vagrant : Vagrantfile $(if $(filter docker,$(VAGRANT_PROVIDER)), $(shell find docker -path "*/$(VAGRANT_HOST)/*" -name "Dockerfile" -print))
	vagrant destroy -f $(VAGRANT_HOST)
	vagrant up $(VAGRANT_HOST)
	touch $@

vagrant/% : .vagrant
	(vagrant status $(VAGRANT_HOST) | grep "$(VAGRANT_HOST)" | grep "running") || vagrant up $(VAGRANT_HOST)
	vagrant ssh $(VAGRANT_HOST) -c 'cd /vagrant && make $(notdir $@)'
	
all-vagrant :
	export VAGRANT_HOST=devel && make vagrant/wheels
	export VAGRANT_HOST=manylinux && make vagrant/wheels
