from typing import List
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class VkGroup(BaseSettings):
    ver: float = Field(...)
    check_interval: int = Field(...)
    access_token: SecretStr = Field(...)
    group_domains: List[str] = Field(...)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        validate_default=False,
        env_prefix="VK_",
    )


class Settings(BaseSettings):
    admins: List[int] = Field(...)
    bot_token: SecretStr = Field(...)
    db_url: str = Field(...)
    ttl_default: int = Field(...)

    vk: VkGroup = Field(...)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        validate_default=False,
    )


config = Settings()
