import pydantic_settings

import lib.app.split_settings as app_split_settings


class Settings(pydantic_settings.BaseSettings):
    api: app_split_settings.ApiSettings = app_split_settings.ApiSettings()
    app: app_split_settings.AppSettings = app_split_settings.AppSettings()
    logger: app_split_settings.LoggingSettings = app_split_settings.LoggingSettings()
