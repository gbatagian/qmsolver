reformat:
	black .
	isort .

test:
	python -m unittest discover tests/

coverage:
	coverage run -m unittest discover tests/
	coverage report

venv:
	pipenv lock
	pipenv install --dev
	pipenv run pre-commit install
	pipenv shell

clean-venv:
	pipenv --rm

install-dev:
	pip install -e .

build:
	python -m build