build:
	rm -rf build/ dist/
# 	python utils/build-pyx-files.py
	python setup.py build_ext --inplace
	python setup.py bdist_wheel

clear:
	rm -rf build/ dist/ *.egg-info
	python utils/cleanup-cython-files.py