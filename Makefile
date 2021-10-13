PYTHON_ENV ?= development
GUNICORN_NUM_WORKERS ?= 5
BIND_HOST ?= 0.0.0.0
BIND_PORT ?= 2400

.PHONY: gunicorn
gunicorn:
	PYTHON_ENV=$(PYTHON_ENV) PYTHONPATH=src/ ./venv/bin/gunicorn --access-logfile - --error-logfile - --workers=$(GUNICORN_NUM_WORKERS) --bind=$(BIND_HOST):$(BIND_PORT) src.server:app

.PHONY: start
start:
	PYTHON_ENV=$(PYTHON_ENV) PYTHONPATH=src/ ./venv/bin/gunicorn --access-logfile - --error-logfile - --workers=$(GUNICORN_NUM_WORKERS) --bind=$(BIND_HOST):$(BIND_PORT) src.server:app

.PHONY: clean
clean:
	find . -name '*.pyc' -delete

.PHONY: package.build
package.build:
	make clean
	./venv/bin/python setup.py sdist
	./venv/bin/python setup.py bdist_wheel

venv:
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip setuptools wheel
	./venv/bin/python -m pip install pip-tools
	./venv/bin/python -m pip install -r requirements.txt
	./venv/bin/python -m pip install -r dev-requirements.txt
	./venv/bin/python -m pip install twine

.PHONY: test
test:
	PYTHON_ENV=test PYTHONPATH=. ./venv/bin/pytest test

.PHONY: package.release
package.release:
	./venv/bin/twine upload dist/*