from src.main.api.models.base_model import BaseModel
# наследуем от модели которую создали сами


# создаем модель через класс
# наследуемся от BaseModel чтобы класс стал моделью пайдантик
class LoginUserRequest(BaseModel):
    username: str
    password: str