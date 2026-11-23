from typing import List, Any

# храним в created_obj созданных нами юзеров(их id) виде массива
class BaseSteps:
    def __init__(self, created_obj: List[Any]):
        self.created_obj = created_obj