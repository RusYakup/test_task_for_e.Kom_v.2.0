import logging
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_COLLECTION: str
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file="./deploy/.env")

    @property
    def URL_DATABASE(self):
        return f"mongodb://{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def logging_config(log_level: str) -> None:
    """
    A function that configures logging based on the input log level.

    :param log_level: The log level to set for the logging configuration.
    :return: None
    """
    numeric_level = getattr(logging, log_level.upper())
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log.info("Logging Configured")
