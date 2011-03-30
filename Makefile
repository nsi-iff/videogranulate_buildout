PYTHON=python

all: clean gstreamer lxml_deps buildout
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

gstreamer:
	sudo apt-get install python-gst0.10 gstreamer-tools -y

lxml_deps:
	sudo apt-get install libxslt1.1 libxslt1-dev libxml2-dev -y

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testVideoGranulate.py

