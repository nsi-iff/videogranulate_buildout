PYTHON=python

all: clean pre_deps bootstrap buildout post_deps
dev: clean pre_deps bootstrap buildout_dev post_deps

clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

pre_deps: pip sys-deps

post_deps: restfulie cyclone should_dsl funkload

sys-deps:
	sudo apt-get install ffmpeg python-imaging python-argparse python-opencv libxslt1.1 libxslt1-dev libxml2-dev python-dev python-setuptools python-webunit python-docutils gnuplot -y

pip:
	easy_install pip

restfulie:
	pip install restfulie

cyclone:
	pip install twisted cyclone

should_dsl:
	pip install should-dsl

funkload:
	pip install funkload

granulate_performance:
	cd tests && python testPerformanceVideoGranulate.py

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

