from typing import Tuple

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.tests.constants import TRANSFER_AMOUNT, FIRST_ACCOUNT_BALANCE, SECOND_ACCOUNT_BALANCE
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.db.crud.account_crud import AccountCrudDb



class TestUserTransfer:
    def test_user_transfer_self_accounts_valid(
            self,
            api_manager: ApiManager,
            accounts_for_transfer,
            db_session: Session
    ):

        user, first_account, second_account = accounts_for_transfer

        transfer_request = AccountTransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=TRANSFER_AMOUNT
        )
        transfer_response = api_manager.user_steps.user_transfer(user, transfer_request)

        assert transfer_response.fromAccountId == first_account.id
        assert transfer_response.toAccountId == second_account.id
        # Проверяем баланс отправителя
        assert transfer_response.fromAccountIdBalance == FIRST_ACCOUNT_BALANCE - TRANSFER_AMOUNT

        #проверяем балансы в бд
        first_account_from_db = AccountCrudDb.get_account_by_id(db_session, first_account.id)
        second_account_from_db = AccountCrudDb.get_account_by_id(db_session, second_account.id)

        assert first_account_from_db.balance == FIRST_ACCOUNT_BALANCE - TRANSFER_AMOUNT, \
            "Баланс отправителя в БД не совпадает с API"
        assert second_account_from_db.balance == SECOND_ACCOUNT_BALANCE + TRANSFER_AMOUNT, \
            "Баланс получателя в БД не совпадает с API"

        # Проверяем баланс получателя через историю транзакций
        receiver_info = api_manager.user_steps.get_account_transactions(
            user, second_account.id
        )
        assert receiver_info.balance == SECOND_ACCOUNT_BALANCE + TRANSFER_AMOUNT, \
            "Баланс получателя в истории транзакций БД не совпадает с API"


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

        assert response.status_code == 400
        assert response.json().get("error") == "Amount must be between 500 and 10000"

        sender_info = api_manager.user_steps.get_account_transactions(
            user, first_account.id
        )

        receiver_info = api_manager.user_steps.get_account_transactions(
            user, second_account.id
        )

        assert sender_info.balance == FIRST_ACCOUNT_BALANCE
        assert receiver_info.balance == SECOND_ACCOUNT_BALANCE

        # провреяем, что балансы не изменились в бд
        first_account_from_db = AccountCrudDb.get_account_by_id(db_session, first_account.id)
        second_account_from_db = AccountCrudDb.get_account_by_id(db_session, second_account.id)

        assert first_account_from_db.balance == FIRST_ACCOUNT_BALANCE, \
            "Баланс отправителя в БД изменился после отказа"
        assert second_account_from_db.balance == SECOND_ACCOUNT_BALANCE, \
            "Баланс получателя в БД изменился после отказа "

