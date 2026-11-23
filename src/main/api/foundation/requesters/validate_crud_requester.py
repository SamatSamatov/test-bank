from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
import allure

# будет распаковывать ответ в модель и возвращать это в тесты
# нужен для позитивных сценариев

class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        # отправляем запрос через круд реквестер, валидейтед нужен только для валидировать модели и давать модели заполененные данными из респонса
        self.crud_requester = CrudRequester( #чтобы не переписывать логику круд реквестера, мы просто вызываем его
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )
    # делаем обертку над нашим круд реквестером чтобы валидировать то что мы получаем в ответе когда нам это нужно
    # и распаковывать это в наши модели
    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        response = self.crud_requester.post(model)
        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validated Model"):
            allure.attach(
                f"Validated Model response: {self.endpoint.value.response_model.__name__}",
                name="Validated model",
                attachment_type=allure.attachment_type.TEXT,
            ) # выдаст имя класса с которым мы работаем
        # валидируем с помощью модели которую прокидывали в эндпоинте с помощью встроенного метода model_validate
        return self.endpoint.value.response_model.model_validate(response.json()) # возвращаем объект пайтонаа с котороым можем работать(распаковка в модель)


    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        with allure.step(
            f"DELETE {Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id} and Validated Model"
        ):
            allure.attach(
                f"Validated Model response: {self.endpoint.value.response_model.__name__}",
                name="Validated model",
                attachment_type=allure.attachment_type.TEXT,
            )
        return self.endpoint.value.response_model.model_validate(response.json())


    def get(self, account_id: int):
        response = self.crud_requester.get(account_id)
        with allure.step(
                f"GET {Config.fetch('backendUrl')}{self.endpoint.value.url} / {account_id} and Validated Model"
        ):
            allure.attach(
                f"Validated Model response: {self.endpoint.value.response_model.__name__}",
                name="Validated model",
                attachment_type=allure.attachment_type.TEXT,
            )
        return self.endpoint.value.response_model.model_validate(response.json())