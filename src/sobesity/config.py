from pydantic import BaseSettings

DB_CONNECTION_TEMPLATE = (
    "{engine}+{dialect}://{username}:{password}@{host}:{port}/{database}"
)


class AppSettings(BaseSettings):
    logger_level: str = "INFO"


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    db: str

    @property
    def url(self):
        return DB_CONNECTION_TEMPLATE.format(
            engine="postgresql",
            dialect="psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    class Config:
        env_prefix = "POSTGRES_"


class JWTSettings(BaseSettings):
    secret: str
    access_token_duration_days: int = 1
    refresh_token_duration_days: int = 30

    class Config:
        env_prefix = "JWT_"


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
