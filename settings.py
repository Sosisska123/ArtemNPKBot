from typing import List
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class VkGroup(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="VK_",
        case_sensitive=False,
        extra="ignore",
    )

    version: str = Field(...)
    check_interval: int = Field(...)
    access_token: SecretStr = Field(...)
    group_domains: List[str] = Field(...)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        validate_default=False,
    )

    admins: List[int] = Field(...)
    bot_token: SecretStr = Field(...)
    db_url: str = Field(...)
    ttl_default: int = Field(...)

    vk: VkGroup = Field(default_factory=VkGroup)


config = Settings()
