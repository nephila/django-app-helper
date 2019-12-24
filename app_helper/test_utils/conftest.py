import pytest


@pytest.fixture(scope="session")
def django_db_setup(request,
                    django_test_environment,
                    django_db_blocker,
                    django_db_use_migrations,
                    django_db_keepdb,
                    django_db_modify_db_settings):
    django_db_blocker.unblock()
