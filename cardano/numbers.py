from decimal import Decimal
from warnings import warn

LOVELACE = Decimal("0.000001")


def to_lovelaces(amount):
    """
    Convert ADA to Lovelaces.

    :param Decimal,int amount:    the amount of ADA
    :rtype: :class:`int`

    """
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
    """
    Convert Lovelaces to ADA.

    :param int amount:  the amount of Lovelaces
    :rtype: :class:`Decimal`
    """
    return (Decimal(amount) * LOVELACE).quantize(LOVELACE)


def as_ada(amount):
    """
    Return the amount rounded to maximal ADA precision.

    :param Decimal,int amount:  the amount to be sanitized
    :rtype: :class:`Decimal` with 6 decimal places precision
    """
    if isinstance(amount, float):
        warn(
            "as_ada() received amount of float type ({:f}). It is STRONGLY DISCOURAGED "
            "to use floating-point numbers for monetary operations due to rounding errors".format(
                amount
            ),
            RuntimeWarning,
        )
    return Decimal(amount).quantize(LOVELACE)
