from pydantic import BaseSettings

DB_CONNECTION_TEMPLATE = (
    "{engine}+{dialect}://{username}:{password}@{host}:{port}/{database}"
)


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

    class Config:
        env_prefix = "JWT_"

class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
