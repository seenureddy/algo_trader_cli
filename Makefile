install-python:
    pip install --upgrade setuptools
    pip install -r test-requirements.txt
    pip install --editable .

code-check:
    ./tools/run_tests.sh -l

coverage:
    pytest --cov-config=.coveragerc --cov=tests/ --cov-report term --cov-report xml:results/coverage.xml --junit-xml=results/test_results.xml

test-all: code-check coverage

deploy-pypi: clear
    python setup.py bdist_wheel

clear:
    rm -rf dist/* results/*
