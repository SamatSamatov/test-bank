from src.main.api.models.base_model import BaseModel
# служит для валидации и распаковки ответа от апи
class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: str