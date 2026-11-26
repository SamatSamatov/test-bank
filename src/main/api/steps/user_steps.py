from typing import List, Any

from src.main.api.foundation.endpoint import Endpoint
from requests import Response
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.models.account_transaction_response import AccountTransactionsResponse
from src.main.api.models.account_transfer_request import AccountTransferRequest
from src.main.api.models.account_transfer_response import AccountTransferResponse
from src.main.api.models.create_user_request import CreateUserRequest, CreateUserRequestCredit
from src.main.api.models.credit_history_response import CreditHistoryResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_user_request import CreditUserRequest
from src.main.api.models.credit_user_response import CreditUserResponse
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps

class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def user_deposit(self, create_user_request: CreateUserRequest, account_deposit_request: AccountDepositRequest) -> AccountDepositResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.USER_DEPOSIT,
            ResponseSpecs.request_ok(),
        ).post(account_deposit_request)
        return response

    def user_deposit_invalid(self, create_user_request: CreateUserRequest, account_deposit_request: AccountDepositRequest) -> Response:
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.USER_DEPOSIT,
            ResponseSpecs.request_bad(),
        ).post(account_deposit_request)
        return response

    def user_transfer(self, create_user_request: CreateUserRequest, account_transfer_request: AccountTransferRequest) -> AccountTransferResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.USER_TRANSFER,
            ResponseSpecs.request_ok(),
        ).post(account_transfer_request)
        return response

    def user_transfer_invalid(self, create_user_request: CreateUserRequest, account_transfer_request: AccountTransferRequest) -> Response:
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.USER_TRANSFER,
            ResponseSpecs.request_bad(),
        ).post(account_transfer_request)
        return response

    def user_credit(self, create_user_request: CreateUserRequestCredit, credit_user_request: CreditUserRequest) -> CreditUserResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created(),
        ).post(credit_user_request)
        return response

    def user_credit_invalid(self, create_user_request: CreateUserRequest, credit_user_request: CreditUserRequest) -> Response:
         response = CrudRequester(
             RequestSpecs.auth_headers(
                 username=create_user_request.username,
                 password=create_user_request.password
             ),
             Endpoint.CREDIT_REQUEST,
             ResponseSpecs.request_bad(),
         ).post(credit_user_request)
         return response

    def credit_repay(self, create_user_request: CreateUserRequestCredit, credit_user_repay: CreditRepayRequest) -> CreditRepayResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username= create_user_request.username,
                password= create_user_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok(),
        ).post(credit_user_repay)
        return response

    def credit_repay_invalid(self, create_user_request: CreateUserRequestCredit, credit_user_repay: CreditRepayRequest) -> Response:
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username= create_user_request.username,
                password= create_user_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable(),
        ).post(credit_user_repay)
        return response

    def user_credit_forbidden(self, create_user_request: CreateUserRequest, credit_user_request: CreditUserRequest) -> Response:
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_forbidden()
        ).post(credit_user_request)
        return response

    def get_account_transactions(self, create_user_request: CreateUserRequest, account_id: int) -> AccountTransactionsResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.ACCOUNT_TRANSACTIONS,
            ResponseSpecs.request_ok()
        ).get(account_id)
        return response

    def get_credit_history(self, create_user_request: CreateUserRequest, account_id: int) -> CreditHistoryResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREDIT_HISTORY,
            ResponseSpecs.request_ok(),
        ).get(account_id)
        return response

    def get_credit_history_raw(self, create_user_request: CreateUserRequest, account_id: int) -> Response:
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.CREDIT_HISTORY,
            lambda r: None
        ).get(account_id)
        return response