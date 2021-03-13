.EXPORT_ALL_VARIABLES:

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

default:
	@echo "Tasks in \033[1;32mvlees-converter\033[0m:"
	@cat Makefile

isset-%:
	@if [ -z '${${*}}' ]; then echo 'ERROR: variable $* not set' && exit 1; fi

notebook:
	@jupyter notebook --ip=0.0.0.0 --allow-root notebooks

lint:
	mypy src/vlees_converter/* --ignore-missing-imports
	flake8 src --ignore=$(shell cat .flakeignore)

dev:
	pip install -e .

test: dev
	pytest --doctest-modules --junitxml=junit/test-results.xml
	bandit -r src -f xml -o junit/security.xml || true

build: clean
	pip install wheel
	python setup.py bdist_wheel

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete
