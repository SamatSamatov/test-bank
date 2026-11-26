from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction

class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_account_id(db: Session, account_id: int) -> list[Transaction]:
        return db.query(Transaction).filter(
            (Transaction.from_account_id == account_id) |
            (Transaction.to_account_id == account_id)
        ).all()

    @staticmethod
    def get_transfer_transactions(db: Session, from_account_id: int, to_account_id: int) -> list[Transaction]:
        return db.query(Transaction).filter_by(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            transaction_type='transfer'
        ).all()