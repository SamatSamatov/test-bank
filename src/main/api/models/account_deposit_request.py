from typing import Annotated
from pydantic import Field
from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

class AccountDepositRequest(BaseModel):
    accountId: int = Field(..., description="ID счёта")
    amount: Annotated[float, CreationRule(min_value=1000, max_value=9000)] = Field(
        ..., gt=0, description="Сумма депозита"
    )