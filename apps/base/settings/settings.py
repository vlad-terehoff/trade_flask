from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    db_url_scheme: str = os.getenv("DB_URL_SCHEME")
    db_host: str = os.getenv("POSTGRES_HOST")
    db_port: str = os.getenv("POSTGRES_PORT")
    db_name: str = os.getenv("POSTGRES_DB_NAME")
    db_user: str = os.getenv("POSTGRES_USER")
    db_password: str = os.getenv("POSTGRES_PASSWORD")
    secret_key: str = os.getenv("SECRET_KEY")
    redis_host: str = os.getenv("REDIS_HOST")
    token: str = os.getenv("TOKEN")
    url_webhook: str = os.getenv("URL_WEBHOOK")
    debug: str = os.getenv("DEBUG")

    @property
    def database_url(self):
        return (f"{self.db_url_scheme}://{self.db_user}:{self.db_password}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}")


settings = Settings()