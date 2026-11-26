from pydantic import Field, ConfigDict

from src.main.api.models.base_model import BaseModel

class CreditUserResponse(BaseModel):
    accountId: int = Field(alias='id', description="BUG: Backend returns 'id' instead of 'accountId'")
    amount: float
    termMonths: int
    balance: float
    creditId: int

model_config = ConfigDict(populate_by_name=True)