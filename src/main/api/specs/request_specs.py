from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
import requests

# тут инкапсулирвана вся логика вся логика подготовки HTTP запросов: заголовки, авторизация и базовая урла
# тесты дергают нужный метод и получают готовый набор параметров для запроса
# так мы избавляемся от дублирования логики и имеем один источник правды

class RequestSpecs:
    # base_headers() базовые заголовки нужны почти любому запросу к апи
    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json", # я шлю json и жду json в ответ
            "accept": "application/json",
        }

# auth_headers делает полный цикл авторизации, чтобы получить токен и приклеить его к заголовкам
# любой тест которому нужен авторизованный запрос вызывает auth_headers и получает готовые заголовки и токен
# получаем метод который который принимает имя и пароль, производит авторизацию, достает из тела ответа токен, прокидывает токен  к базовым хедерам

    @staticmethod
    def auth_headers(username: str, password: str):
        #создает модель запроса LoginUserRequest(username=username, password=password) - типизирванное представление тела будущего запроса
        request = LoginUserRequest(username=username, password=password)
        # шлем post на url передавая request.model_dump()(тело) и базовые заголовки base_headers()
        response = requests.post(
            url=f"{Config.fetch("backendUrl")}/auth/token/login",
            json=request.model_dump(),
            # обращаемся к нашему классу и обратиться к нашим базовым хедерам
            headers=RequestSpecs.base_headers()
        ) # если ответ 200 то
        if response.status_code == 200:
            # распаковываем json в модель LoginUserResponse - это гарантия, что ответ действително содержит нужные поля(например токен)
            response_data = LoginUserResponse(**response.json())
            # получаем токен из response_data
            token = response_data.token
            # вызываем base_headers() и сохраняем в словарь headers, сейчас в нем 2 ключа
            headers = RequestSpecs.base_headers()
            # добавляем к headers Authorization: Bearer <token>
            # добавляем в словарь headers ключ Authorization с значением f"Bearer {token}"
            headers["Authorization"] = f"Bearer {token}"
            #возвращаем словарь с хедерами и базовой урлой
            return headers # возвращаем просто headers без ключа
        # если не 200 то кидаем Exception("Failed to login")
        raise Exception("Failed to login")


# unauth_headers() возвращает те же headers и base_url, но без Authorization
# нужен для запросов где не требуется авторизация
    @staticmethod
    def unauth_headers():
        return  RequestSpecs.base_headers()



# Спека	        Что описывает	        Кто готовит  	Что внутри
# request_spec	как отправить запрос	RequestSpecs	заголовки + base_url