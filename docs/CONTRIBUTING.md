To start to contribute, install the dependencies (Python >= 3.6)
```
python3 -m venv venv
pip install -e .
pip install -r test-requirements.txt
```
Fork this repository, make the changes into the forked repository and push a new Merge Request to 'main' branch.
Open an issue in case of big MRs.
# Testing
To run the tests, start a new Driver as server on port `9999`, for example:
```
./chromedriver --port=9999
```
And execute the tests
```
python -m pytest -n auto
```