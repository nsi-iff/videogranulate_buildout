PYTHON=python

all: clean pre_deps bootstrap buildout post_deps
dev: clean pre_deps bootstrap buildout_dev post_deps

clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

pre_deps: pip pil lxml_deps argparse ffmpeg

post_deps: restfulie cyclone should_dsl funkload

ffmpeg:
	sudo apt-get install ffmpeg -y

pip:
	easy_install pip

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

funkload:
	sudo apt-get install python-dev python-setuptools python-webunit python-docutils gnuplot
	pip install funkload

load_test:
	bin/videogranulate_ctl start
	bin/add-user.py test test
	cd tests && fl-run-bench testFunkLoad.py VideoGranulateBench.test_granulate
	cd tests && fl-build-report --html videogranulate-bench.xml -r funkload_report
	bin/videogranulate_ctl stop
	bin/del-user.py test

load_test_report:
	cd tests && fl-build-report --html videogranulate-bench.xml -r funkload_report

bootstrap:
	$(PYTHON) bootstrap.py

buildout:
	bin/buildout -vv

buildout_dev:
	bin/buildout -vvc develop.cfg

test:
	cd tests && $(PYTHON) testVideoGranulate.py

