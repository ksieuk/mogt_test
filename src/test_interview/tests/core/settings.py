import pydantic_settings

import tests.core.split_settings as app_split_settings


class TestsSettings(pydantic_settings.BaseSettings):
    api: app_split_settings.ApiSettings = app_split_settings.ApiSettings()
    project: app_split_settings.ProjectSettings = app_split_settings.ProjectSettings()


tests_settings = TestsSettings()
