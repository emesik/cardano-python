import collections
from decimal import Decimal
from warnings import warn

LOVELACE = Decimal("0.000001")


def to_lovelaces(amount):
    """Convert ADA decimal to integer of Lovelaces."""
    if not isinstance(amount, (Decimal, int, float)):
        raise ValueError(
            "Amount '{}' doesn't have numeric type. Only Decimal, int and "
            "float (not recommended) are accepted as amounts."
        )
    if isinstance(amount, float):
        warn(
            "to_lovelaces() received amount of float type ({:f}). It is STRONGLY DISCOURAGED "
            "to use floating-point numbers for monetary operations due to rounding errors".format(
                amount
            ),
            RuntimeWarning,
        )
    return int(amount * 10 ** 6)


def from_lovelaces(amount):
    """Convert amount of Lovelaces to ADA decimal."""
    return (Decimal(amount) * LOVELACE).quantize(LOVELACE)


def as_ada(amount):
    """Return the amount rounded to maximal ADA precision."""
    if isinstance(amount, float):
        warn(
            "as_ada() received amount of float type ({:f}). It is STRONGLY DISCOURAGED "
            "to use floating-point numbers for monetary operations due to rounding errors".format(
                amount
            ),
            RuntimeWarning,
        )
    return Decimal(amount).quantize(LOVELACE)


BlockPosition = collections.namedtuple(
    "BlockPosition", ["epoch", "slot", "absolute_slot"]
)
