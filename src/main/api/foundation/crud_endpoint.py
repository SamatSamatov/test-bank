# служит для усиления контрактности
from typing import Protocol, Optional

from requests import Response

from src.main.api.models.base_model import BaseModel


# Protocol описывает интерфейс для статической провреки типов без необходимости наследования
# если наш класс будет реализовывать методы CrudEndpoint с правильной инфраструктурой, то он будет совеместим с этим протоколом и сразу будет проверка типов
# наследоваться необязательно, можно реализовывать его методы с теми же сигнатурами
class CrudEndpoint(Protocol):
    # для всех ручек возвращаем либо модель либо респонс в сыром виде
    # post получает модель
    # get получает айди 
    # def post принимает тело запроса, возвращает базовую модель(позитив) или сырой респонс(негатив)
    def post(self, model: Optional[BaseModel]) -> BaseModel | Response: ... # служит контрактом
    def get(self, user_id: int) -> BaseModel | Response:...
    def delete(self, user_id: int) -> BaseModel| Response:...