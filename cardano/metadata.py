_MININT = -(2 ** 64) - 1
_MAXINT = 2 ** 64 - 1


class Metadata(dict):
    @staticmethod
    def validate_key(key):
        if not isinstance(key, int):
            raise KeyError("Metadata keys must be integers")
        if key < 0:
            raise KeyError("Metadata key {:d} is negative".format(key))
        if key > _MAXINT:
            raise KeyError("Metadata key {:d} is over 2^64-1".format(key))
        return key

    @staticmethod
    def validate_value(val):
        if isinstance(val, (str, bytes, bytearray)):
            if len(val) > 64:
                raise ValueError(
                    "The string {} is too long ({:d} > 64)".format(val, len(val))
                )
        elif isinstance(val, int):
            if val < _MININT:
                raise ValueError("Int {:d} is less than -2^64-1".format(val))
            elif val > _MAXINT:
                raise ValueError("Int {:d} is over 2^64-1".format(val))
        elif isinstance(val, list):
            if len(set(map(type, val))) > 1:
                raise ValueError(
                    "The list assigned to key {:d} consists of different types"
                )
        elif isinstance(val, dict):
            for k, v in val.items():
                Metadata.validate_value(k)
                Metadata.validate_value(v)
        else:
            raise TypeError(
                "Metadata values must be of int, str, bytes, bytearray, lists of thereof or another Metadata instances, not {}".format(
                    str(type(val))
                )
            )
        return val

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            for k, v in args[0]:
                Metadata.validate_key(k)
                Metadata.validate_value(v)
        super(Metadata, self).__init__(*args, **kwargs)

    def __setitem__(self, key, val):
        return super(Metadata, self).__setitem__(
            Metadata.validate_key(key), Metadata.validate_value(val)
        )
