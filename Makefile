PYTHON=python

all: clean gstreamer pil lxml_deps argparse buildout nsisvgtool nsigranulate restfulie cyclone should-dsl
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

argparse:
	sudo apt-get install python-argparse -y

pil:
	sudo apt-get install python-imaging

gstreamer:
	sudo apt-get install python-gst0.10 gstreamer-tools gstreamer0.10-ffmpeg gnome-core -y

lxml_deps:
	sudo apt-get install libxslt1.1 libxslt1-dev libxml2-dev python-dev -y

restfulie:
	pip install restfulie

cyclone:
	pip install twisted cyclone

nsisvgtool:
	@rm -Rf nsi.svgtool-0.3
	@rm -rf nsi.svgtool-0.3.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.svgtool-0.3.tar.gz
	tar -vzxf nsi.svgtool-0.3.tar.gz
	cd nsi.svgtool-0.3 && ${PYTHON} setup.py install
	@rm -Rf nsi.svgtool-0.3
	@rm -rf nsi.svgtool-0.3.tar.gz

nsigranulate:
	@rm -Rf nsi.granulate-0.10.2
	@rm -rf nsi.granulate-0.10.2.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.granulate-0.10.2.tar.gz
	tar -vzxf nsi.granulate-0.10.2.tar.gz
	cd nsi.granulate-0.10.2 && ${PYTHON} setup.py install
	@rm -Rf nsi.granulate-0.10.2
	@rm -rf nsi.granulate-0.10.2.tar.gz

should_dsl:
	pip install should-dsl

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testVideoGranulate.py

