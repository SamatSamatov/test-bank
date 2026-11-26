# тут будем инициализировать апи менеджера, чтобы его можно было прокидывать в тесты безопасно без импортов, а через фикстурвы
import pytest
from src.main.api.classes.api_manager import ApiManager

@pytest.fixture
def api_manager(created_obj):
    return ApiManager(created_obj)


