from typing import Annotated
from pydantic import Field
from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class CreditUserRequest(BaseModel):
    accountId: int = Field(..., description="ID счёта")

    # Валидный диапазон по бизнес-логике (от 5000 до 15000)
    amount: Annotated[float, CreationRule(min_value=5000, max_value=15000)] = Field(
        ..., gt=0, description="Сумма кредита"
    )

    # Валидный диапазон по Swagger (от 1 до 60)
    termMonths: Annotated[int, CreationRule(min_value=1, max_value=60)] = Field(
        ..., ge=1, le=60, description="Срок в месяцах"
    )