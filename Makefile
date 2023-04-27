all: build

build: format clean test
	python setup.py sdist bdist_wheel
	echo 'finished'

.PHONY: test
test:
	coverage run -m pytest -vv .
	coverage report -m
	flake8

.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -f .coverage
	rm -f coverage.xml
	find . | grep -E '(__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf

.PHONY: format
format:
	black .
