PYTHON_BUILD_ENV=$(PWD)/build_env
PYTHON_BUILD_BIN=$(PYTHON_BUILD_ENV)/bin/python3

build-env:
	@python3 -m venv $(PYTHON_BUILD_ENV)
	@$(PYTHON_BUILD_BIN) -m pip install --upgrade pip==23.0.1
	@$(PYTHON_BUILD_BIN) -m pip install -r "$(PWD)/requirements-build-env.txt"

unit-tests:
	@echo "Run unit tests"

build:
	@$(PYTHON_BUILD_BIN) -m build

clean:
	@rm -rf "$(PWD)/build_env" "$(PWD)/dist"
	@find $(PWD) -type d -name "*egg-info" -exec rm -rf {} +
