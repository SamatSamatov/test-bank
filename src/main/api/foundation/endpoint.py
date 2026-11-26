# тут будут храниться все эндпоинты и реквест респонс модели для централизованного упраления
from dataclasses import dataclass # подходит для небольших моделей похож на пидантик класс, менее гибок, хранит в себе встроенные методы __eq__, __repr__
from enum import Enum

from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.models.account_transaction_response import AccountTransactionsResponse
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.account_transfer_response import AccountTransferResponse
from src.main.api.models.base_model import BaseModel
from typing import Optional, Type

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_history_response import CreditHistoryResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_user_request import CreditUserRequest
from src.main.api.models.credit_user_response import CreditUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@dataclass
class EndpointConfiguration:
    # описываем что мы будем создавать
    url: str
    request_model: Optional[Type[BaseModel]] # не у всех запросов есть модели, поэтому делаем оптионал, все модели имеют тип бейс модел тк наследуются от базовой модели
    response_model: Optional[Type[BaseModel]]

# тут будут храниться все наши эндпоинты, инфа о реквест модели, урл, респонс модели
class Endpoint(Enum): # делаем енум чтобы можно было обращаться к полям как к значениям и использовать их в CrudRequester
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url = "/admin/create",
        response_model = CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = "/admin/users", # id будем цеплять в реквестере
        response_model = None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model = LoginUserRequest,
        url = "/auth/token/login",
        response_model = LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model = None,
        url = "/account/create",
        response_model = CreateAccountResponse
    )

    USER_DEPOSIT = EndpointConfiguration(
        request_model = AccountDepositRequest,
        url = "/account/deposit",
        response_model = AccountDepositResponse
    )

    USER_TRANSFER = EndpointConfiguration(
        request_model = AccountTransferRequest,
        url = "/account/transfer",
        response_model = AccountTransferResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        request_model = CreditUserRequest,
        url = "/credit/request",
        response_model = CreditUserResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        request_model = CreditRepayRequest,
        url = "/credit/repay",
        response_model = CreditRepayResponse
    )

    ACCOUNT_TRANSACTIONS = EndpointConfiguration(
        request_model = None,
        url = "/account/transactions",
        response_model = AccountTransactionsResponse
    )

    CREDIT_HISTORY = EndpointConfiguration(
        request_model = None,
        url = "/credit/history",
        response_model = CreditHistoryResponse
    )