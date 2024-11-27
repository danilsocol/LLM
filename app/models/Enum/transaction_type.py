import enum


class TransactionType(enum.Enum):
    SPEND = "spend"
    DEPOSIT = "deposit"