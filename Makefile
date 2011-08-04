PYTHON=python

all: clean pil lxml_deps argparse buildout restfulie cyclone should-dsl
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

argparse:
	sudo apt-get install python-argparse -y

pil:
	sudo apt-get install python-imaging

lxml_deps:
	sudo apt-get install libxslt1.1 libxslt1-dev libxml2-dev python-dev -y

restfulie:
	pip install restfulie

opencv:
	sudo apt-get install libcv4 libhighgui4 python-opencv

cyclone:
	pip install twisted cyclone

should_dsl:
	pip install should-dsl

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testVideoGranulate.py

