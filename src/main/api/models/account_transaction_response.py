from typing import List, Optional
from src.main.api.models.base_model import BaseModel


class TransactionResponse(BaseModel):
    transactionId: int
    type: str
    amount: float

    # Делаем поля опциональными, так как при депозите fromAccountId может быть null,
    # а при выводе toAccountId может быть null
    fromAccountId: Optional[int] = None
    toAccountId: Optional[int] = None

    createdAt: str


class AccountTransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List["TransactionResponse"]


# В самом низу файла
AccountTransactionsResponse.model_rebuild()
