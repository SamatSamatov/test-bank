from typing import Annotated
from pydantic import Field
from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

class AccountTransferRequest(BaseModel):
    fromAccountId: int = Field(..., description="ID счета отправителя")
    toAccountId: int = Field(..., description="ID счета получателя")
    amount: Annotated[float, CreationRule(min_value=500, max_value=2000)] = Field(
        ..., gt=0, description="Сумма депозита"
    )