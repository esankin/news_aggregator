from pydantic import BaseSettings


class Settings(BaseSettings):
    backend_secret: str
    postgres_user: str
    postgres_password: str

    redis_host: str = 'redis'
    redis_port: int = 6379

    class Config:
        secrets_dir = '/run/secrets'


settings = Settings()