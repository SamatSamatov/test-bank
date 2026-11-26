def calculate_safe_transfer_amount(initial_balance: float) -> float:
    return initial_balance * 0.5


def calculate_expected_balance(
    initial_balance: float,
    amount: float,
    is_debit: bool
) -> float:
    if is_debit:
        return initial_balance - amount
    return initial_balance + amount