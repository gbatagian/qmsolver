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
	pipenv shell

install-dev:
	pip install -e .

build:
	python -m build

check-build:
	python -m twine check dist/*

upload-test:
	python -m twine upload --repository testpypi dist/*