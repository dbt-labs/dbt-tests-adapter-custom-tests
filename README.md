# Getting started with the dbt testing framework

["Testing a new adapter"](https://docs.getdbt.com/docs/contributing/testing-a-new-adapter) describes three broad categories of tests enabled by the [`dbt-tests-adapter`](https://github.com/dbt-labs/dbt-core/tree/HEAD/tests/adapter) Python package:
- Basic tests for adapter plugins
- Optional tests tests for adapter plugins
- **Custom test cases** (this repo)

It also introduces these concepts:
- Modifying test cases
- Running with multiple profiles

## Install

See [here](https://docs.python.org/3/library/venv.html#creating-virtual-environments) for instructions that will work for your operating system and shell. These instructions are for `zsh` and `bash`:
```shell
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt -r dev-requirements.txt
source env/bin/activate
```

## Run

Run all the tests:
```shell
python3 -m pytest
```

There are many options for invoking `pytest` and choosing which tests to execute. See [here](https://docs.pytest.org/usage.html) for the `pytest` documentation. Some common options are included below.

### Run tests in a module
```shell
python3 -m pytest tests/functional/example/test_example_failing_test.py
```

### Run tests in a directory
```shell
python3 -m pytest tests/functional
```

## Checklist to make it your own

The repo provides custom versions of `test.env`, `test.env.sample`, and `requirements.txt` for demonstration purposes, and you will likely want to modify them if applying the `dbt-tests-adapter` framework to your own projects.

Here's a quick checklist of items to review:
- [ ] Add `test.env` to the `.gitignore` file (since it will likely contain secrets)
- [ ] Populate `test.env.sample` with the environment variables within `conftest.py::dbt_profile_target`
- [ ] Review the contents of `requirements.txt` to deem if each entry is applicable
