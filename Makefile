build:
	rm -rf build/ dist/
#	python utils/build-pyx-files.py
	python setup.py build_ext --inplace
	python setup.py bdist_wheel

setenv:
	python3.7 -m venv venv
	. venv/bin/activate
	pip install --upgrade pip setuptools wheel
	pip install -r test-requirements.txt
	pip install -r dev-requirements.txt

test:
	pytest -n auto

linter:
	black -l 100 .
	isort --profile black --line-length 100 caqui tests
	flake8 --exclude venv*,.tox,build,*/test_process_data.py --max-line-length 100
	mypy caqui tests --config=pyproject.toml    

clear:
	rm -rf build/ dist/ *.egg-info
	python utils/cleanup-cython-files.py