from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestSpecs

# выносим в отдельный слой подготовку данных которые мы передаем в нужный реквестер валидейт или круд реквестер
class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest): # получает тело запроса
        # создаём пользователя через валидирующий реквестер
        # на выходе получаем готовую Pydantic-модель созданного пользователя
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)
        # после создания юзера
        self.created_obj.append(response) # после возвращаения объекта внутрь наших тестов(он заполняется данными), \сюда возвращается объект, делается аппенд, добавляется тело и потом выполянется teardown
        return response  # возвращаем респонс из степы

    def delete_user(self, user_id: int):
        CrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)

    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad()
        ).post(create_user_request)

    def login_user(self, login_user_request: LoginUserRequest):
        # используем Validate так как нам нужно тело ответа
        response = ValidateCrudRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_ok()
        ).post(login_user_request)
        return response