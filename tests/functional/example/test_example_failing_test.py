import pytest
import os
from pathlib import Path
from dbt.tests.util import run_dbt, check_relations_equal

# our file contents
from tests.functional.example.fixtures import (
    my_seed_csv,
    my_model_sql,
    my_model_yml,
)
# complement a _real_ downstream model to test using fake upstream relations
from tests.functional.example.fixture_model_unit_test import (
    upstream_model_1,
    upstream_model_2,
    expected,
)


# class must begin with 'Test'
class TestGenericTestExample:
    """
    Methods in this class will be of two types:
    1. Fixtures defining the dbt "project" for this test case.
       These are scoped to the class, and reused for all tests in the class.
    2. Actual tests, whose names begin with 'test_'.
       These define sequences of dbt commands and 'assert' statements.
    """
    
    # install this repo as a package
    @pytest.fixture(scope="class")
    def packages(self):
        return {"packages": [{"local": os.getcwd()}]}

    # configuration in dbt_project.yml
    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
          "name": "example",
          "models": {"+materialized": "view"}
        }

    # everything that goes in the "seeds" directory
    @pytest.fixture(scope="class")
    def seeds(self):
        return {
            "my_seed.csv": my_seed_csv,
        }

    # everything that goes in the "models" directory
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "my_model.sql": my_model_sql,
            "my_model.yml": my_model_yml,
        }

    # The actual sequence of dbt commands and assertions
    # pytest will take care of all "setup" + "teardown"
    def test__expected_failure__option_1a(self, project):
        """
        Deps, then seed, then run, then test. We expect one of the tests to fail
        An alternative pattern is to use pytest "xfail" (see below)
        Another alternative is to use `pytest.raises()` (see below)
        """
        # install packages
        run_dbt(["deps"])
        # seed seeds
        run_dbt(["seed"])
        # run models
        run_dbt(["run"])
        # test tests
        results = run_dbt(["test", "--select", "test_type:generic"], expect_pass = False)  # expect failing test
        result_statuses = sorted(r.status for r in results)

        # we expect a single failure; nothing more, nothing less
        assert result_statuses == ["fail"]

    def test__expected_failure__option_1b(self, project):
        """
        Deps, then build (which includes seed, run, and test). We expect one of the tests to fail
        An alternative pattern is to use pytest "xfail" (see below)
        Another alternative is to use `pytest.raises()` (see below)
        """
        # install packages
        run_dbt(["deps"])
        # build
        results = run_dbt(["build", "--exclude", "test_type:singular"], expect_pass = False)  # expect failing test
        result_statuses = sorted(r.status for r in results)

        # expect test to fail after seed and run succeed
        assert result_statuses == ["fail", "success", "success"]

        # this would also work instead of an explicit list of statuses
        assert "fail" in result_statuses

        # or count the number of expected failures
        assert result_statuses.count("fail") == 1

    @pytest.mark.xfail
    def test__expected_failure__option_2a(self, project):
        """Expect a failing test using xfail with any Exception"""
        # install packages
        run_dbt(["deps"])
        # seed, run, test
        run_dbt(["build"])

    @pytest.mark.xfail(raises=AssertionError)
    def test__expected_failure__option_2b(self, project):
        """Expect a failing test using xfail with a specific Exception"""
        # install packages
        run_dbt(["deps"])
        # seed, run, test
        run_dbt(["build"])

    def test__expected_failure__option_3a(self, project):
        """Expect a failing test using a specific Exception"""
        # install packages
        run_dbt(["deps"])

        with pytest.raises(AssertionError):
            # seed, run, test
            run_dbt(["build"])

    def test__expected_failure__option_3b(self, project):
        """Expect a failing test using a specific Exception and message"""
        # install packages
        run_dbt(["deps"])

        with pytest.raises(AssertionError, match=r"dbt exit state did not match expected"):
            # seed, run, test
            run_dbt(["build"])

    def test__expected_failure__option_3c(self, project):
        """Expect a failing test using any Exception"""
        # install packages
        run_dbt(["deps"])

        with pytest.raises(Exception):
            # seed, run, test
            run_dbt(["build"])


class TestSingularTestExample:
    @pytest.fixture(scope="class")
    def packages(self):
        return {"packages": [{"local": os.getcwd()}]}

    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
          "name": "example",
          "models": {"+materialized": "view"}
        }

    @pytest.fixture(scope="class")
    def seeds(self):
        return {
            "my_seed.csv": my_seed_csv,
        }

    @pytest.fixture(scope="class")
    def models(self):
        return {
            "my_model.sql": my_model_sql,
        }

    def test__expected_failure__option_3c(self, project):
        """Expect a failing test using any Exception"""
        run_dbt(["deps"])

        with pytest.raises(AssertionError):
            run_dbt(["build"])


class TestModelBuildExample:

    @pytest.fixture(scope="class")
    def seeds(self):
        # fake the upstream data used by the model
        return {
            "upstream_model_1.csv": upstream_model_1,
            "upstream_model_2.csv": upstream_model_2,
            "expected.csv": expected,
        }

    @pytest.fixture(scope="class")
    def models(self):
        # pull the actual SQL for the downstream model from the filesystem
        model_name = "downstream_model.sql"
        model_path = Path(f"models/example/{model_name}")
        sql_contents = ""
        with open(model_path) as f:
            sql_contents = f.read()

        return {
            model_name: sql_contents,
        }

    def test__what_to_expect(self, project):
        """TODO - Don't know what to expect!"""
        # Install and build
        run_dbt(["deps"])
        run_dbt(["build"])

        # check relations equal
        check_relations_equal(project.adapter, ["downstream_model", "expected"])
