
# Setting up python precommit plugin

The precommit plugin modifies the project so that every time you perform a commit, it checks (or fixes) certain issues that you would otherwise be bothered with.

This is convenient provided it is fast; we have to keep it fast!


## Install precommit
	venv/bin/activate
	echo pre-commit > devtools.txt
	pip install -r devtools.txt

## Generate a sample config

	pre-commit sample-config > .pre-commit-config.yaml

## My tested configuration


	-   repo: https://github.com/pre-commit/pre-commit-hooks
	    rev: v4.4.0
	    hooks:
	    -   id: trailing-whitespace
	    -   id: end-of-file-fixer
	    -   id: check-yaml
	    -   id: check-added-large-files
	    -   id: name-tests-test
	-   repo: https://github.com/psf/black
	    rev: 23.3.0
	    hooks:
	      - id: black
	        language_version: python 3
	-   repo: local
	    hooks:
	    -   id: run_tests
	        language: script
	        name: Run Tests
	        entry: ./runtests
	        stage: [commit]

## Create a batch file to run tests

	#!/bin/bash
	. venv/bin/activate
	pytest


## Add pytest to the config


	pre-commit autoupdate
	pre-commit run


## Go!
When you do a commit, the plugins will run.
