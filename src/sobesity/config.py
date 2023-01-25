from pydantic import BaseSettings

DB_CONNECTION_TEMPLATE = (
    "{engine}+{dialect}://{username}:{password}@{host}:{port}/{database}"
)


class DatabaseSettings(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DB: str

    @property
    def url(self):
        return DB_CONNECTION_TEMPLATE.format(
            engine="postgresql",
            dialect="psycopg2",
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            database=self.DB,
        )

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()

