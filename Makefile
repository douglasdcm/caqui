build:
	rm -rf build/ dist/
#	python utils/build-pyx-files.py
	python setup.py build_ext --inplace
	python setup.py bdist_wheel

setenv:
	# Get the list of envs and run on all of them
	python3.7 -m venv venv
	. venv/bin/activate
	pip install --upgrade pip setuptools wheel
	pip install -r test-requirements.txt
	pip install -r requirements.txt

PARAMS ?= ''
test:
	pytest $(PARAMS)

linter:
	black -l 100 . --include caqui,tests
	isort --profile black --line-length 100 caqui tests
	flake8 --exclude venv*,.tox,build,*/test_process_data.py,_vendor --max-line-length 100
	mypy caqui tests --config=pyproject.toml    

coverage:
	coverage run --source='caqui' -m pytest
	coverage report
	coverage html

clear:
	rm -rf build/ dist/ *.egg-info
	python utils/cleanup-cython-files.py