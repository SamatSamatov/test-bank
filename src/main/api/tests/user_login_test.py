import pytest

from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.classes.api_manager import ApiManager



@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username, \
            f"Имя пользователя {login_user_request.username} в запросе не совпадает с именем пользователя {response.user.username} в ответе"
        assert response.user.role == "ROLE_ADMIN", \
            f"Роль {response.user.role} не совпадает с отправленной ролью ROLE_ADMIN"


    def test_login_user(self, api_manager: ApiManager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, \
            f"Имя пользователя {create_user_request.username} в запросе не совпадает с именем пользователя {response.user.username} в ответе"
        assert response.user.role == "ROLE_USER", \
            f"Роль пользователя {response.user.role} не свовпадает с отправленной ролью ROLE_USER"