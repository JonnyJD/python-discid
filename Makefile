version := 1.2.0

build:
	python setup.py build

sdist:
	python setup.py sdist

upload: sdist
	twine3 upload -s dist/discid-$(version).tar.gz

check:
	python setup.py test -vv

check2:
	python2 setup.py test -vv

disccheck:
	python setup.py test -vv --tests test_discid.TestDisc

disccheck2:
	python2 setup.py test -vv --tests test_discid.TestDisc

doc:
	cd doc && make dirhtml

version:
	sed -i -e 's/\(__version__\s=\s"\)[0-9.]\+[0-9a-z.-]*/\1$(version)/' \
		discid/__init__.py
	sed -i -e 's/\(version="\)[0-9.]\+[0-9a-z.-]*/\1$(version)/' \
		setup.py

clean:
	rm -f *.pyc discid/*.pyc
	rm -rf __pycache__ discid/__pycache__

.PHONY: doc build
