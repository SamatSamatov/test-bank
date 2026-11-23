from requests import Response
from http import HTTPStatus

# тут будут храниться методы которые будут проверять статус коды
# создаем функцию внутри функции(замыкание) чтобы сохранять параметры и для откладывания провреки по респонсу
# респонс может приходить не сразу, а после отправки запроса
class ResponseSpecs:
    @staticmethod
    # реквест ок будет возврщать сам конфирм
    # реквест ок как шаблон, а конфирм как реализция
    # как только получаем респонс, он попадает в конфирм, потом ассерт и из реквест ок будет возвращаться конфирм
    def request_ok():
        # конфирм принимает тип респосе из библиотеки requests
        def confirm(response: Response): # конфирм отрабатывет только когда мы получим респонс
            assert response.status_code == HTTPStatus.OK, response.text # елси не ок(200 статус) то вернет response.text
        return confirm

    @staticmethod
    def request_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text # CREATED == 201
        return confirm

    @staticmethod
    # создаем для негативного теста
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text # BAD_REQUEST == 400
        return confirm

    @staticmethod
    def request_unprocessable():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text
        return confirm

    @staticmethod
    def request_forbidden():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text
        return confirm

# Спека	        Что описывает	        Кто готовит	    Что внутри
# response_spec	что ожидать в ответе	ResponseSpecs	функция-проверка confirm(response)

