from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.generators.model_generator import RandomModelGenerator
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

        credit_request = RandomModelGenerator.generate(
            CreditUserRequest,
            accountId=account.id
        )

        credit_response = api_manager.user_steps.user_credit(
            user,
            credit_request
        )

        assert credit_response.amount == credit_request.amount, \
            f"Сумма кредита запроса {credit_request.amount} не совпадает с суммой кредита ответа {credit_response.amount}"
        assert credit_response.balance == credit_request.amount, \
            f"Баланс кредита при выдаче {credit_response.balance} не равен сумме {credit_request.amount} запрошенного кредита кредита"
        assert credit_response.accountId == account.id, \
            f"ID счета {account.id} не свпадает с ID счета {credit_response.accountId} полученного кредита "
        assert credit_response.creditId is not None, \
            "У созданного кредита должен быть creditId"

        #Проверки БД
        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, credit_response.creditId)

        assert credit_from_db is not None, \
            "Кредит не найден в БД"
        assert credit_from_db.amount == credit_request.amount, \
            f"Сумма кредита {credit_from_db.amount} в БД не совпадает с суммой запроса {credit_request.amount}"

        # [BUG] Бэкенд записывает в БД отрицательный баланс
        assert credit_from_db.balance == -credit_request.amount, \
            f"Баланс в БД {credit_from_db.balance} не совпадает с текущим (багованным) поведением бэкенда {-credit_request.amount}"

        assert credit_from_db.term_months == credit_request.termMonths, \
            f"Срок кредита в БД {credit_from_db.term_months} не совпадает со сроком запроса {credit_request.termMonths}"
        assert credit_from_db.account_id == account.id, \
            f"ID счёта в БД {credit_from_db.account_id} не совпадает с ID счета {account.id}"


    def test_credit_request_invalid(
            self,
            api_manager: ApiManager,
            created_account,
            db_session: Session
    ):
        user, account = created_account

        credit_user_request =  RandomModelGenerator.generate(
            CreditUserRequest,
            accountId=account.id
        )

        credit_user_response = api_manager.user_steps.user_credit_forbidden(
            user,
            credit_user_request
        )

        assert credit_user_response.status_code == 403, \
            f"Ожидали (есть действующий кредит) 403, но получили {credit_user_response.status_code}"

        credit_info = api_manager.user_steps.get_credit_history_raw(
            user,
            account.id
        )
        assert credit_info.status_code == 404, \
            f"Ожидали 404 (кредитов нет), но получили {credit_info.status_code}"

        credits = CreditCrudDb.get_credit_by_account_id(db_session, account.id)
        assert len(credits) == 0, \
            "Кредит появился в БД, хотя должен был быть отклонён"