
IMAGE:= daytona-builder

# disable __pycache__

export PYTHONDONTWRITEBYTECODE=y

#
# Static Analysis
#

check-flake8:
# From the suggested workflow

# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

PYTHON_FILES:= $(shell find -name "*.py" -type f)
check-pylint:
# Implicit .pylintrc
	PYLINTHOME=. python3 -m pylint $(PYTHON_FILES)

check: check-flake8 check-pylint

#
# Unit Test
#

COVERAGE:= --cov=daytona --cov-branch --no-cov-on-fail --cov-report=term-missing
test:
	PYTHONPATH=. pytest -x $(COVERAGE) tests

#
# Docker
#

image:
	docker build -t $(IMAGE) .

#
# Usual boring stuff
#

.PHONY: check check-flake8 check-pylint test image

# EOF
