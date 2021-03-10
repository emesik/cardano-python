import enum


class Era(enum.IntEnum):
    """
    Represents Cardano era, a distinct phase of platform development.
    """
    BYRON = 1
    SHELLEY = 2
    GOGUEN = 3
    BASHO = 4
    VOLTAIRE = 5
