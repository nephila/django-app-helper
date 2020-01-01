.PHONY: clean-pyc clean-build docs bump-dev release upload

help:
	@echo "clean - Cleanup all artifacts"
	@echo "clean-build - Remove build artifacts"
	@echo "clean-pyc - Remove Python file artifacts"
	@echo "lint - Check code style"
	@echo "test - Run tests in current environment"
	@echo "test-all - Run tests on every environment version with tox"
	@echo "coverage - Check code coverage in current environment"
	@echo "upload - Upload package to PyPi"
	@echo "release - Build package"
	@echo "tag-dev - Create dev release"

clean: clean-build clean-pyc

clean-build:
	python setup.py clean --all
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	tox -epep8,isort,black

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage erase
	coverage run setup.py test
	coverage report -m

upload: release
	twine upload dist/*

tag-dev:
	bumpversion --list patch --message="Bump develop version [ci skip]" --no-tag

release: clean
	python -m pep517.build .
