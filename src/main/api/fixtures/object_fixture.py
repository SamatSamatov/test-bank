# тут будем создавать юзера и чистить данные
# тут будет полноценная чистка и создание листа
import pytest
from typing import List, Any

import logging

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def created_obj():
    objects: List[Any] = [] # objects это будет список который будет хранить какой то тип данных эни, будет делаться до
    yield objects # отдаем по одному тем самым передаем в тест
    clean_user(objects) # функция для очистки юзеров


# clean_user служит для очистки тестовых юзеров - из объекта получаем их айди и передаем в удаление
def clean_user(objects: List[Any]):
    api_manager = ApiManager(objects) # вызываем апи менеджер и передаем ему объект/ тут будут храниться модели по CreateUserResponse
    for u in objects: # итерируемся по элементам которые есть в объектах
        if isinstance(u, CreateUserResponse): # является ли u экземляром класса CreateUserResponse
            api_manager.admin_steps.delete_user(u.id) # передаем в степу - из степы в реквестер и таким образом мы будем удалять нашего юзера
        else: # если не относится то будем это логгировать
            logging.warning(f"Error in delete user_id: {u.id}") # указываем айли юзера которого не смогли удалить