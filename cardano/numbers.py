from decimal import Decimal

LOVELACE = Decimal("0.000001")


def to_lovelaces(amount):
    """Convert ADA decimal to integer of Lovelaces."""
    if not isinstance(amount, (Decimal, int, float)):
        raise ValueError(
            "Amount '{}' doesn't have numeric type. Only Decimal, int and "
            "float (not recommended) are accepted as amounts."
        )
    return int(amount * 10 ** 6)


def from_lovelaces(amount):
    """Convert amount of Lovelaces to ADA decimal."""
    return (Decimal(amount) * LOVELACE).quantize(LOVELACE)


def as_ada(amount):
    """Return the amount rounded to maximal ADA precision."""
    return Decimal(amount).quantize(LOVELACE)
