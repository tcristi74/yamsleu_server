import os


class DbConfig:
    def __init__(self):
        self.db_config = {
            'username': os.getenv("DB_USERNAME"),
            'password': os.getenv("DB_PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT"),
            'database': os.getenv("DB_NAME")
        }

    def get_config(self):
        return self.db_config
