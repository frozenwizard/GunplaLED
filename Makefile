
.PHONY: clean
clean:
	rm -rf target/
	rm -rf micropython/

.PHONY: setup
setup:
	mkdir micropython
	wget -P micropython https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2
	cp src/config.py.template src/config.py
	#install pip3
	# pip install rshell

.PHONY: install-micropython
install-micropython:
	$(eval RASPI_MOUNT=$(shell findmnt -t vfat -o TARGET | grep RPI))
	@echo Installing micropython to $(RASPI_MOUNT)
	cp micropython/* $(RASPI_MOUNT)

.PHONY: build-test
build-test:
	rm -rf target/
	mkdir target/
	cp src/test.py target/main.py

.PHONY: build
build:
	rm -rf target/
	mkdir target/
	cp -r src/phew/ target/phew
	cp src/config.py target/
	cp src/index.html target/
	cp src/nu_gundam.py target/
	cp src/nu_gundam.json target/
	cp src/webserver.py target/main.py

.PHONY: deploy
deploy:
	~/.local/bin/rshell rm -r /pyboard/*
	~/.local/bin/rshell cp -r target/* /pyboard/