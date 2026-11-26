import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.tests.constants import FIRST_ACCOUNT_BALANCE, SECOND_ACCOUNT_BALANCE
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.utils.helpers import calculate_expected_balance, calculate_safe_transfer_amount



class TestUserTransfer:
    def test_user_transfer_self_accounts_valid(
            self,
            api_manager: ApiManager,
            accounts_for_transfer,
            db_session: Session
    ):

        user, first_account, second_account = accounts_for_transfer

        safe_amount = calculate_safe_transfer_amount(FIRST_ACCOUNT_BALANCE)

        transfer_request = RandomModelGenerator.generate(
            AccountTransferRequest,
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=safe_amount
        )
        transfer_response = api_manager.user_steps.user_transfer(user, transfer_request)

        expected_sender_balance = calculate_expected_balance(
            FIRST_ACCOUNT_BALANCE, safe_amount, is_debit=True
        )
        expected_receiver_balance = calculate_expected_balance(
            SECOND_ACCOUNT_BALANCE, safe_amount, is_debit=False
        )

        # Деньги списаны с правильного счёта отправителя
        assert transfer_response.fromAccountId == first_account.id, \
            f"Ожидали счёт отправителя {first_account.id}, но получили {transfer_response.fromAccountId}"

        # Деньги зачислены на правильный счёт получателя
        assert transfer_response.toAccountId == second_account.id, \
            f"Ожидали счёт получателя {second_account.id}, но получили {transfer_response.toAccountId}"

        # Баланс отправителя уменьшился на сумму перевода
        assert transfer_response.fromAccountIdBalance == expected_sender_balance, \
            f"Ожидали баланс отправителя {expected_sender_balance}, но получили {transfer_response.fromAccountIdBalance}"

        #проверяем балансы в бд
        first_account_from_db = AccountCrudDb.get_account_by_id(db_session, first_account.id)
        second_account_from_db = AccountCrudDb.get_account_by_id(db_session, second_account.id)

        assert first_account_from_db.balance == expected_sender_balance, \
            f"Ожидали баланс отправителя в БД {expected_sender_balance}, но получили {first_account_from_db.balance}"
        assert second_account_from_db.balance == expected_receiver_balance, \
            f"Ожидали баланс получателя в БД {expected_receiver_balance}, но получили {second_account_from_db.balance}"


    @pytest.mark.parametrize("invalid_transfer_amount",[499,10001])
    def test_user_transfer_self_accounts_invalid(
            self,
            api_manager,
            accounts_for_transfer,
            invalid_transfer_amount,
            db_session: Session
    ):

        user, first_account, second_account = accounts_for_transfer

        transfer_request = AccountTransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=invalid_transfer_amount
        )

        response = api_manager.user_steps.user_transfer_invalid(user, transfer_request)

        assert response.status_code == 400, \
            f"Ожидали 400, получили {response.status_code}"
        assert response.json().get("error") == "Amount must be between 500 and 10000", \
            "Текст ошибки не сопадает с текстом ошибки из Swagger"

        sender_info = api_manager.user_steps.get_account_transactions(
            user, first_account.id
        )

        receiver_info = api_manager.user_steps.get_account_transactions(
            user, second_account.id
        )

        assert sender_info.balance == FIRST_ACCOUNT_BALANCE, \
            f"Баланс отправителя {sender_info.balance} из истории транзакций изменился"
        assert receiver_info.balance == SECOND_ACCOUNT_BALANCE, \
            f"Баланс получателя {receiver_info.balance} из истории транзакций изменился"

        # провреяем, что балансы не изменились в бд
        first_account_from_db = AccountCrudDb.get_account_by_id(db_session, first_account.id)
        second_account_from_db = AccountCrudDb.get_account_by_id(db_session, second_account.id)

        assert first_account_from_db.balance == FIRST_ACCOUNT_BALANCE, \
            "Баланс отправителя в БД изменился после отказа"
        assert second_account_from_db.balance == SECOND_ACCOUNT_BALANCE, \
            "Баланс получателя в БД изменился после отказа "

