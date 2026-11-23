from pathlib import Path
from typing import Any

class Config:
    _isinstance = None
    _dictionary = {}

    def __new__(cls):
        if cls._isinstance is None:
            cls._isinstance = super(Config, cls).__new__(cls)

            config_path = Path(__file__).parents[4] / 'resources' / 'urls.properties'

            if not config_path.exists():
                raise FileNotFoundError(f"Config path not found: {config_path}")

            with open(config_path, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.split("=")
                        cls._dictionary[key] = value.strip()

        return cls._isinstance

    # нужен для того чтобы передавать сюда ключь - словарь подхватывал этот ключь и искал значение по ключу
    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        # если обратиться к несуществующему ключу то будет ошибка, но .get(key, default_value) позволяет вернуть дефолтное значение
        return Config()._dictionary.get(key, default_value)
