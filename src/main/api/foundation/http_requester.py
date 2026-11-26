# будет овечать за логику за которую отвечал Requester
from src.main.api.foundation.endpoint import Endpoint
from typing import Dict, Callable

# ничего не наследует - получает реквест спеку, эндпоинт с классом эндпоинт, ресопнс спеку
# в отедльном классе эндпоинт - все эндпоинты, в реквест спеке будут храниться только хедеры
class HttpRequester:
    def __init__(self, request_spec: dict, endpoint: Endpoint, response_spec: Callable):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec