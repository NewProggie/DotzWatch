export PYTHONPATH=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

init:
	pip install -r requirements.txt

test:
	pytest -v tests

coverage:
	coverage run --source=dotzwatch -m pytest tests
	coverage report

doc:
	pydoc -g dotzwatch

clean:
	find . -name *.pyc -exec rm -rf {} \;
	rm -rf htmlcov .cache
