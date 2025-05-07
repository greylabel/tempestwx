.PHONY: integration_tests lint unit_tests

install:
	@echo poetry install
	poetry install

install_dev:
	@echo poetry install
	poetry install

unit_tests:
	@echo unit test...
	python -m pytest ./tests/unit

pylint:
	@echo lint
	pylint .

flake8:
	flake8 . --count --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

lint: pylint flake8

isort:
	isort . --check-only --diff
