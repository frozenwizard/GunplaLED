
.PHONY: clean
clean:
	rm -rf target/
	rm -rf micropython/

.PHONY: setup
setup:
	mkdir micropython
	wget -P micropython https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2
	cp src/config.py.template src/settings.py
	#install pip3
	# pip install rshell

.PHONY: install-micropython
install-micropython:
	$(eval RASPI_MOUNT=$(shell findmnt -t vfat -o TARGET | grep RPI))
	@echo Installing micropython to $(RASPI_MOUNT)
	cp micropython/* $(RASPI_MOUNT)

install-micropython-osx:
	cp micropython/* /Volumes/RPI-RP2/

.PHONY: build-test
build-test:
	rm -rf target/
	mkdir target/
	cp src/test.py target/main.py

.PHONY: build
build:
	rm -rf target/
	mkdir target/
	mkdir target/config
	mkdir target/www
	cp -r src/phew/ target/phew
	cp src/settings.py target/
	cp -r src/www/ target/www/
	cp src/nu_gundam.py target/
	cp src/LED.py	target/
	cp src/BaseGundam.py target/
	cp src/config/nu_gundam.json target/config/nu_gundam.json
	cp src/webserver.py target/main.py

.PHONY: deploy
deploy:
	rshell rm -r /pyboard/*
	rshell cp -r target/* /pyboard/