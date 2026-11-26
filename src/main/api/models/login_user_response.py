from src.main.api.models.base_model import BaseModel

# из за вложенности создаем отдельную модель
# поле user в LoginUserResponse будет обращаться к модели User
class User(BaseModel):
    username: str
    role: str

class LoginUserResponse(BaseModel):
    token: str
    user: User
