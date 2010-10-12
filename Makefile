PYTHON=python

all: clean gstreamer buildout
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

gstreamer:
	sudo apt-get install python-gst0.10 gstreamer-tools

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testVideoGranulate.py

