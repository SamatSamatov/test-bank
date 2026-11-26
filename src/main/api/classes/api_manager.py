from typing import List, Any

from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps


# апи менеджер будет овечать за хранение всех степов
# тк апи менеджер хранит все шаги мы можем черезе него мы можем через него прокидывать нужные данные для шагов
# откуда то из прокидывать данные которые нужны всем шагам а апи менеджер сможет прокидывать это всем шагам
class ApiManager:
    # created_obj который мы сделали в базовой модели BaseSteps
    def __init__(self, created_obj: List[Any]):
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)