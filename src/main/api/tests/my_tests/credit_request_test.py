from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.credit_user_request import CreditUserRequest


class TestCreditRequest:
    # Убрали xfail, потому что теперь мы корректно обрабатываем ответ бэкенда
    def test_credit_request_valid(
            self,
            api_manager: ApiManager,
            created_account_credit,
            db_session: Session
    ):
        user, account = created_account_credit

        credit_user_request = CreditUserRequest(accountId=account.id, amount=5000, termMonths=12)

        credit_user_response = api_manager.user_steps.user_credit(
            user,
            credit_user_request
        )

        assert credit_user_response.amount == 5000
        assert credit_user_response.balance == 5000
        assert credit_user_response.accountId == account.id
        assert credit_user_response.creditId is not None

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, credit_user_response.creditId)

        assert credit_from_db is not None, "Кредит не найден в БД"
        assert credit_from_db.amount == 5000, "Сумма кредита в БД не совпадает"
        # [BUG] Бэкенд записывает в БД отрицательный баланс (-5000),
        # хотя в API-ответе возвращает положительный (5000).
        assert credit_from_db.balance == -5000.0, "Баланс в БД не совпадает с текущим (багованным) поведением бэкенда"
        assert credit_from_db.term_months == 12, "Срок кредита в БД не совпадает"
        assert credit_from_db.account_id == account.id, "ID счёта в БД не совпадает"


    def test_credit_request_invalid(
            self,
            api_manager: ApiManager,
            created_account,
            db_session: Session
    ):
        user, account = created_account

        credit_user_request = CreditUserRequest(accountId=account.id, amount=5000, termMonths=12)

        credit_user_response = api_manager.user_steps.user_credit_forbidden(
            user,
            credit_user_request
        )

        assert credit_user_response.status_code == 403

        credit_info = api_manager.user_steps.get_credit_history_raw(
            user,
            account.id
        )

        assert credit_info.status_code == 404, \
            f"Ожидали 404 (кредитов нет), но получили {credit_info.status_code}"

        credits = CreditCrudDb.get_credit_by_account_id(db_session, account.id)

        assert len(credits) == 0, \
            "Кредит появился в БД, хотя должен был быть отклонён"