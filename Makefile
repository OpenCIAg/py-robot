PYTHON?=$(shell [ -f venv/bin/python ] && echo 'venv/bin/python' ||  echo 'python')
COVERAGE?=$(shell [ -f venv/bin/coverage ] && echo 'venv/bin/coverage' ||  echo 'coverage')

venv:
	python3.6 -m venv venv

pip: venv
	$(PYTHON) -m pip install -r requirements.txt

pip-dev: pip
	$(PYTHON) -m pip install -r requirements-dev.txt

test: pip-dev
	$(PYTHON) -m unittest discover -s "tests/unit" -p "test_*.py"

test-all: pip-dev
	$(PYTHON) -m unittest discover -s "tests/" -p "test_*.py"

coverage: pip-dev
	$(COVERAGE) run -m unittest discover -s "tests/unit" -p "test_*.py"
	$(COVERAGE) html --include="robot/*"

coverage-all: pip-dev
	$(COVERAGE) run -m unittest discover -s "tests/" -p "test_*.py"
	$(COVERAGE) html --include="robot/*"
	$(PYTHON) -mwebbrowser htmlcov/index.html &

clean:
	rm -f $(shell find . -name "*.pyc")
	rm -rf htmlcov/ coverage.xml .coverage
	rm -rf dist/ build/
	rm -rf *.egg-info