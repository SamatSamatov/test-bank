from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.api.configs.config import Config
# движок будет управлять соединением с базой 
engine = create_engine(
    Config.fetch("dataBaseUrl"),
    echo=False,
    connect_args={'client_encoding': 'utf8'}
) # отключаем логи скл echo=False
SessionLocal = sessionmaker(bind=engine) # sessionmaker фабрика сессий необходима для создания объекта сессии чтобы мы молгил работать бд - удалять, обновлять, читать
