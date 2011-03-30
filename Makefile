PYTHON=python

all: clean gstreamer lxml_deps buildout nsisvgtool nsigranulate
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

gstreamer:
	sudo apt-get install python-gst0.10 gstreamer-tools -y

lxml_deps:
	sudo apt-get install libxslt1.1 libxslt1-dev libxml2-dev -y

nsisvgtool:
	@rm -Rf nsi.svgtool-0.3
	@rm -rf nsi.svgtool-0.3.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.svgtool-0.3.tar.gz
	tar -vzxf nsi.svgtool-0.3.tar.gz
	cd nsi.svgtool-0.3 && ${PYTHON} setup.py install
	@rm -Rf nsi.svgtool-0.3
	@rm -rf nsi.svgtool-0.3.tar.gz


nsigranulate:
	@rm -Rf nsi.granulate-0.9.3
	@rm -rf nsi.granulate-0.9.3.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.granulate-0.9.3.tar.gz
	tar -vzxf nsi.granulate-0.9.3.tar.gz
	cd nsi.granulate-0.9.3 && ${PYTHON} setup.py install
	@rm -Rf nsi.granulate-0.9.3
	@rm -rf nsi.granulate-0.9.3.tar.gz

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testVideoGranulate.py

