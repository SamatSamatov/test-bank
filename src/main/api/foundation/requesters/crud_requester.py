from typing import Optional

import requests
from requests import Response
import allure

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel

# централизованный реквестер с универсальными методами 
# наследует HttpRequester который отвечает за все параметры для запросов
# CrudRequester реализует два метода пост и делит, тк для тестов нам нужны только эти два метода

class CrudRequester(HttpRequester): # нужен для негативных сценариве где нужен сырой ответ
    # получаем тело внутри модели
    def post(self, model: Optional[BaseModel]) -> Response:
        # перевродим в формат воспринимаемый сервером(в словарь), если нет модели то возвращаем пустоту
        body = model.model_dump() if model is not None else ""
        url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}"
        # для метода пост формируем запрос (делает все то что мы делали в наших реквестерах)
        with allure.step(f"Post {url}"):
            allure.attach(
                str(body),
                "Request body",
                allure.attachment_type.JSON
            )
            response = requests.post(
            # строим полный путь
                url=url, # берем урл в зависимости от переданного эндпоинта(например ADMIN_CREATE_USER)
                headers=self.request_spec, # получаем из HttpRequester
                json=body,
            )
            allure.attach(
                response.text,
                "Response body",
                allure.attachment_type.JSON
            )

        self.response_spec(response) # чекаем response в response_spec(проверяем статус код)
        return response

    def delete(self, user_id: int) -> Response:
        url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}"

        with allure.step(f"Delete {url}"):
            response = requests.delete(
                url=url,
                headers=self.request_spec
            )
            allure.attach(
                response.text or "<empty>",
                "Response body",
                allure.attachment_type.TEXT
            )

        self.response_spec(response)
        return response

    def get(self, account_id: int) -> Response:
        url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{account_id}"
        with allure.step(f"Get {url}"):
            response = requests.get(
                url=url,
                headers=self.request_spec,
            )
            allure.attach(
                response.text,
                "Response body",
                allure.attachment_type.JSON
            )

        self.response_spec(response)
        return response