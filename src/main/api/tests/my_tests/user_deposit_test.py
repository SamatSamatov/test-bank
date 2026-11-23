import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb


class TestUserDeposit:
    def test_user_deposit_valid(
            self,
            api_manager: ApiManager,
            deposit_request,
            db_session: Session
    ):
        user, account, request = deposit_request

        initial_balance = account.balance

        deposit_response = api_manager.user_steps.user_deposit(
            user,
            request
        )

        assert deposit_response.balance == initial_balance + request.amount
        assert deposit_response.id == request.accountId

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == initial_balance + request.amount, \
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

        initial_balance = account.balance

        invalid_request = AccountDepositRequest(
            accountId=account.id,
            amount=amount
        )

        response = api_manager.user_steps.user_deposit_invalid(user, invalid_request)

        assert response.json().get("error") == "Amount must be between 1000 and 9000"
        assert initial_balance == 0

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == initial_balance, "Баланс счета в БД не равен 0"
