test:
	python -m unittest discover -s "tests/unit" -p "test_*.py"

test-all:
	python -m unittest discover -s "tests/" -p "test_*.py"

coverage:
	coverage run -m unittest discover -s "tests/unit" -p "test_*.py"
	coverage html --include="asterisk/*"

coverage-all:
	coverage run -m unittest discover -s "tests/" -p "test_*.py"
	coverage html --include="asterisk/*"
	python -mwebbrowser htmlcov/index.html &

clean:
	rm -f $(shell find . -name "*.pyc")
	rm -rf htmlcov/ coverage.xml .coverage
	rm -rf dist/ build/
	rm -rf *.egg-info