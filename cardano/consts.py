import enum


class Era(enum.IntEnum):
    """
    Represents Cardano era, a distinct phase of platform development.

    .. warning:: **Do NOT use the integer values directly.**
                There are new Eras being introduced, as for example Allegra and Mary were
                inserted as stepping stones into full Goguen. However, you may use comparison
                operators between them, to check which was earlier or later than the other one.
    """

    BYRON = 1
    SHELLEY = 2
    ALLEGRA = 3
    MARY = 4
    GOGUEN = 5
    BASHO = 6
    VOLTAIRE = 7
