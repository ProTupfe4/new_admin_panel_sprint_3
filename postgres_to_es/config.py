from typing import List

import backoff
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from logger import logger


class PostgresDsn(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")
    dbname: str = Field(..., alias="POSTGRES_DB", env="POSTGRES_DB")
    user: str = Field(..., alias="POSTGRES_USER", env="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD", env="POSTGRES_PASSWORD")
    host: str = Field(..., alias="POSTGRES_HOST", env="POSTGRES_HOST")
    port: str = Field(..., alias="POSTGRES_PORT", env="POSTGRES_PORT")


class ElasticDsn(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")
    host: str = Field(..., alias="ELASTICSEARCH_HOST", env="ELASTICSEARCH_HOST")
    port: str = Field(..., alias="ELASTICSEARCH_PORT", env="ELASTICSEARCH_PORT")


class RedisDsn(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")
    host: str = Field(..., alias="REDIS_HOST", env="REDIS_HOST")
    port: str = Field(..., alias="REDIS_PORT", env="REDIS_PORT")


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")
    batch_size: int = Field(..., alias="BATCH_SIZE", env="BATCH_SIZE")
    scan_frequency: int = Field(..., alias="SCAN_FREQ", env="SCAN_FREQ")
    backoff_max_retries: int = (
        Field(..., alias="BACKOFF_MAX_RETRIES", env="BACKOFF_MAX_RETRIES"),
    )
    elasticsearch_indexes: List[str] = Field(
        ..., alias="ELASTICSEARCH_INDEXES", env="ELASTICSEARCH_INDEXES"
    )


POSTGRES_DSN = PostgresDsn()
ELASTIC_DSN = ElasticDsn()
REDIS_DSN = RedisDsn()
APP_SETTINGS = AppSettings()


BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "logger": logger,
    "max_tries": APP_SETTINGS.backoff_max_retries,
}

STATE_ROOT = "last_movies_updated"

STATE_KEY = "updated"

MOVIE_INDEX = "movies"
