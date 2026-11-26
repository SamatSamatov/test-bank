import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.utils.helpers import calculate_expected_balance


class TestUserDeposit:
    def test_user_deposit_valid(
            self,
            api_manager: ApiManager,
            deposit_request,
            db_session: Session
    ):
        user, account, request = deposit_request

        deposit_response = api_manager.user_steps.user_deposit(
            user,
            request
        )

        expected_balance = calculate_expected_balance(
            account.balance,
            request.amount,
            is_debit=False
        )

        assert deposit_response.balance == expected_balance, \
            f"Баланс после депозита {deposit_response.balance} не увеличился на сумму пополнения {request.amount}"
        assert deposit_response.id == request.accountId, \
            f"ID счёта в ответе {deposit_response.id} не совпадает с ID из запроса {request.accountId}"

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == account.balance + request.amount, \
            "Баланс счёта в БД не совпадает с API после депозита"


    @pytest.mark.parametrize("amount",[999,9001])
    def test_user_deposit_invalid(
            self,
            amount: int,
            api_manager: ApiManager,
            created_account,
            db_session: Session
    ):
        user, account = created_account

        invalid_request = AccountDepositRequest(
            accountId=account.id,
            amount=amount
        )

        response = api_manager.user_steps.user_deposit_invalid(user, invalid_request)

        assert response.json().get("error") == "Amount must be between 1000 and 9000", \
            "Текст ошибки не совпадает с текстом ошибки из swagger"
        assert account.balance == 0, \
            f"Начальный баланс {account.balance} счета изменился после невалидного запроса на пополнение"

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == account.balance, "Баланс счета в БД не равен 0"
