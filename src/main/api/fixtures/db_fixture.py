import pytest
from src.main.api.db.engine import SessionLocal, engine
# создаем сессию при помощи которой будем работать с бд, то есть отправлять ей запросы
#  каждый отдельный тест будет получать абсолютно новый, независимый экземпляр того, что возвращает эта фикстура(сессия и транзакция)
@pytest.fixture(scope="function") # каждый тест рабоатет в рамках своей сессии, чтобы данные никак не конкорировали и не затирались
def db_session():
    connection = engine.connect() # создаем соеднинение с базой через движок
    transaction = connection.begin() # контейнер операций с бд
    session = SessionLocal(bind=connection)
    try: # отдаем сессию
        yield session
    finally: # то что просходит в любом случае
        session.close() # закрытие сессии
        transaction.rollback() # откат всех изменений
        connection.close() # заккрытие коннекта
