import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_request import CreateUserRequestCredit
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_user_request import CreditUserRequest
from src.main.api.tests.constants import FIRST_ACCOUNT_BALANCE, SECOND_ACCOUNT_BALANCE


# формирует запрос на создание польхователя, получать пользователя и отдавать данные
@pytest.fixture
def create_user_request(api_manager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request # можем обращаться к полям так как отдаем модель

@pytest.fixture
def create_user_request_role_credit(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequestCredit)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def created_account(api_manager, create_user_request) -> tuple[CreateUserRequest, CreateAccountResponse]:
    account = api_manager.user_steps.create_account(create_user_request)
    return create_user_request, account

@pytest.fixture
def created_account_credit(api_manager, create_user_request_role_credit) -> tuple[CreateUserRequest, CreateAccountResponse]:
    account = api_manager.user_steps.create_account(create_user_request_role_credit)
    return create_user_request_role_credit, account

@pytest.fixture
def accounts_for_transfer(api_manager, create_user_request) -> tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse]:
    # создаем юзера и делаем ему два счета
    user = create_user_request

    first_account = api_manager.user_steps.create_account(user)
    second_account = api_manager.user_steps.create_account(user)
    # делаем депозит на первый счет
    first_deposit = AccountDepositRequest(
        accountId= first_account.id,
        amount= FIRST_ACCOUNT_BALANCE
    )
    api_manager.user_steps.user_deposit(user, first_deposit)
    # делаем депозит на второй счет
    second_deposit = AccountDepositRequest(
        accountId= second_account.id,
        amount= SECOND_ACCOUNT_BALANCE
    )
    api_manager.user_steps.user_deposit(user, second_deposit)

    # возыврщвем юзера, первый счет(уже с деньгами) и второй счет
    return user, first_account, second_account

@pytest.fixture
def account_for_credit_repay(api_manager, create_user_request_role_credit) -> tuple[CreateUserRequest, CreateAccountResponse, CreditUserResponse]:
    user = create_user_request_role_credit
    account = api_manager.user_steps.create_account(user)

    credit_request = RandomModelGenerator.generate(
        CreditUserRequest,
        accountId=account.id
    )

    credit_response = api_manager.user_steps.user_credit(user, credit_request)
    return user, account, credit_response


@pytest.fixture
def paid_credit_account(api_manager, create_user_request_role_credit) -> tuple[CreateUserRequest, CreateAccountResponse, CreateAccountResponse]:
    """
    Пользователь + счёт + полностью погашенный кредит.
    Возвращает: user, account, credit_response, balance_after_repay
    """
    user = create_user_request_role_credit

    # ШАГ 1: Создаём аккаунт
    account = api_manager.user_steps.create_account(user)

    # ШАГ 2: Создаём кредит (ИСПОЛЬЗУЕМ user_credit, а НЕ credit_repay!)
    credit_request = CreditUserRequest(
        accountId=account.id,
        amount=5000,
        termMonths=12
    )
    credit_response = api_manager.user_steps.user_credit(user, credit_request)  # ← user_credit!

    # ШАГ 3: Полностью погашаем кредит
    repay_request = CreditRepayRequest(
        creditId=credit_response.creditId,
        accountId=account.id,
        amount=credit_response.amount
    )
    api_manager.user_steps.credit_repay(user, repay_request)  # ← credit_repay!

    # ШАГ 4: Баланс после погашения = 0 (кредит удалён из истории)
    balance_after_repay = 0.0

    return user, account, credit_response, balance_after_repay


@pytest.fixture
def deposit_request(created_account) -> tuple[CreateUserRequest, CreateAccountResponse, AccountDepositRequest]:
    create_user_request, account = created_account
    request = RandomModelGenerator.generate(
        AccountDepositRequest,
        accountId=account.id
    )
    return create_user_request, account, request