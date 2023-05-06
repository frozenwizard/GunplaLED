.DEFAULT_GOAL=help

.PHONY: clean
clean:  ##Nukes the target and micropython dirs
	rm -rf target/
	rm -rf micropython/

.PHONY: setup
setup:  ## Downloads and setups required dependencies
	mkdir micropython
	wget -P micropython https://micropython.org/resources/firmware/rp2-pico-w-20230426-v1.20.0.uf2
	cp src/config.py.template src/settings.py
	#install pip3
	# pip install rshell

.PHONY: install-micropython-ubuntu
install-micropython-ubuntu:  ## Installs micropython to pi board on ubuntu
	$(eval RASPI_MOUNT=$(shell findmnt -t vfat -o TARGET | grep RPI))
	@echo Installing micropython to $(RASPI_MOUNT)
	cp micropython/* $(RASPI_MOUNT)

.PHONY: install-micropython-osx
install-micropython-osx:  ## Installs micropython to pi board on Mac OSX
	cp micropython/* /Volumes/RPI-RP2/

.PHONY: build-test
build-test:  ## Builds a test script to sanity check deployments
	rm -rf target/
	mkdir target/
	cp src/test.py target/main.py

.PHONY: build
build:  ## Builds the server and Gunpla
	rm -rf target/
	mkdir target/
#	mkdir target/config
#	mkdir target/www
#	cp -r src/phew/ target/phew
#	cp src/settings.py target/
#	cp -r src/www/ target/www/
#	cp src/nu_gundam.py target/
#	cp src/LED.py	target/
#	cp src/BaseGundam.py target/
	cp -r src/ target/
	#cp src/config/nu_gundam.json target/config/nu_gundam.json
	#cp src/webserver.py target/main.py
	#mv target/webserver.py target/main.py

.PHONY: deploy
deploy:  ## Deploys the built artifacts to the pi board
	rshell rm -r /pyboard/*
	rshell cp -r target/* /pyboard/

#python tooling
.PHONY: format
format:  ## Format the Python code
	autopep8 -i -r src/

.PHONY: lint
lint: ## Lints the python code
	pylint src/
	

help:  ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
