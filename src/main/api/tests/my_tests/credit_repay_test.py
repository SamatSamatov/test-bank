from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.credit_repay_request import CreditRepayRequest



class TestCreditRepay:
    def test_credit_repay_valid(
            self,
            api_manager: ApiManager,
            account_for_credit_repay,
            db_session: Session
    ):
        user, account, credit_response = account_for_credit_repay

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account.id,
            amount=credit_response.amount
        )

        credit_repay_response = api_manager.user_steps.credit_repay(user, credit_repay_request)

        assert credit_repay_response.creditId == credit_repay_request.creditId
        assert credit_repay_response.amountDeposited == credit_repay_request.amount

        credit_history_response = api_manager.user_steps.get_credit_history_raw(user, account.id)

        assert credit_history_response.status_code == 404, \
            f"Ожидали 404 (кредит удалён после погашения), но получили {credit_history_response.status_code}"

        # проверки бд
        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == 0, \
            f"Баланс счёта в БД не обнулился после погашения: {account_from_db.balance}"

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db is None or credit_from_db.balance == 0.0, \
            "Кредит не удалён и баланс не обнулён в БД после погашения"

    def test_credit_repay_already_paid(
            self,
            api_manager: ApiManager,
            paid_credit_account,
            db_session: Session
    ):
        user, account, credit_response, balance_after_repay = paid_credit_account

        # Пытаемся погасить ПОВТОРНО
        second_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account.id,
            amount=credit_response.amount
        )
        response = api_manager.user_steps.credit_repay_invalid(user, second_repay_request)

        # Проверяем отказ
        assert response.status_code in [404, 422]

        # проверки бд
        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == balance_after_repay, \
            f"Баланс счёта изменился. Было {balance_after_repay}, стало {account_from_db.balance}"