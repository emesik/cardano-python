from decimal import Decimal
import operator

_MININT = -(2 ** 64 - 1)
_MAXINT = 2 ** 64 - 1


class Metadata(dict):
    """
    Represents Cardano transaction metadata. Inherits from :class:`dict` but passes all keys
    and values through validity check.

    :param mapping:         a sequence of (key, value) pairs
    """

    TYPE_RESOLVERS = {
        "string": lambda s: s,
        "int": lambda i: Metadata.deserialize_int(i),
        "bytes": bytes.fromhex,
        "list": lambda l: [
            Metadata.TYPE_RESOLVERS[k](v)
            for k, v in map(
                operator.itemgetter(0),
                map(list, map(operator.methodcaller("items"), l)),
            )
        ],
        "map": lambda m: Metadata.deserialize_map(m),
    }

    @staticmethod
    def validate_key(key):
        """
        Checks if the key is allowed, i.e. is an :class:`int` and within the allowed range.

        Raises :class:`KeyError` otherwise.
        """
        if not isinstance(key, int):
            raise KeyError("Metadata keys must be integers")
        if key < 0:
            raise KeyError("Metadata key {:d} is negative".format(key))
        if key > _MAXINT:
            raise KeyError("Metadata key {:d} is over 2^64-1".format(key))
        return key

    @staticmethod
    def validate_value(val):
        """
        Checks if the value is allowed, i.e. is one of :class:`int`, :class:`str`, :class:`bytes`,
        :class:`bytearray`, :class:`list` or :class:`dict`.

        Raises :class:`TypeError` otherwise. Also raises :class:`ValueError` if the value is of
        proper type but exceeds range limit for Cardano metadata.
        """
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
        elif isinstance(val, (list, tuple)):
            pass
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

    @staticmethod
    def serialize_value(val):
        """
        Serializes Python value to an object that can be passed to transaction as a metadata value.
        The returned object is a mapping which contains both the type name and the value.

        Raises :class:`RuntimeError` when a value of unrecognized type has been passed.
        """
        if isinstance(val, int):
            return {"int": val}
        elif isinstance(val, str):
            return {"string": val}
        elif isinstance(val, (bytes, bytearray)):
            return {"bytes": val.hex()}
        elif isinstance(val, list):
            return {"list": [Metadata.serialize_value(i) for i in val]}
        elif isinstance(val, dict):
            return {
                "map": [
                    {"k": Metadata.serialize_value(k), "v": Metadata.serialize_value(v)}
                    for k, v in val.items()
                ]
            }
        # This should never happen
        raise RuntimeError(
            "Found unserializable value of {} (type {})".format(val, str(type(val)))
        )

    def serialize(self):
        """
        Returns serialized form of the metadata, which can be passed to the transaction.
        """
        return {str(k): Metadata.serialize_value(v) for k, v in self.items()}

    @staticmethod
    def deserialize_item(key, vdata):
        if len(vdata) > 1:
            raise ValueError(
                "The value dict for key {:s} has {:d} members while only one is permitted".format(
                    key, len(vdata)
                )
            )
        typename = list(vdata.keys()).pop()
        val = list(vdata.values()).pop()
        return {int(key): Metadata.TYPE_RESOLVERS[typename](val)}

    @staticmethod
    def deserialize_int(i):
        if isinstance(i, int):
            return i
        elif isinstance(i, Decimal):
            return int(i.quantize(1))
        raise TypeError("Got int serialized as {} of value {}".format(str(type(i)), i))

    @staticmethod
    def deserialize_map(themap):
        data = {}
        for m in themap:
            ktype, kval = list(m["k"].items()).pop()
            vtype, vval = list(m["v"].items()).pop()
            key = Metadata.TYPE_RESOLVERS[ktype](kval)
            if isinstance(key, list):
                key = tuple(key)
            elif isinstance(key, dict):
                key = ImmutableDict(key)
            data[key] = Metadata.TYPE_RESOLVERS[vtype](vval)
        return data

    @staticmethod
    def deserialize(txdata):
        """
        Deserializes transaction metadata :class:`dict` and returns :class:`Metadata` instance.

        :param txdata:  the transaction data
        """
        data = {}
        for key, vdata in txdata.items():
            data.update(Metadata.deserialize_item(key, vdata))
        return Metadata(data.items())

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


class ImmutableDict(dict):
    """
    A flavor of ``dict`` with all mutating methods blocked and hash generation added.
    It can be used as mapping keys.
    """

    def __hash__(self):
        return hash(
            "|".join(
                [
                    "{}={}".format(*i)
                    for i in sorted(self.items(), key=operator.itemgetter(0))
                ]
            )
        )

    def __setitem__(self, key, value):
        raise RuntimeError("ImmutableDict doesn't allow changes")

    def __delitem__(self, key):
        raise RuntimeError("ImmutableDict doesn't allow changes")

    def clear(self):
        raise RuntimeError("ImmutableDict doesn't allow changes")

    def pop(self, key):
        raise RuntimeError("ImmutableDict doesn't allow changes")

    def popitem(self):
        raise RuntimeError("ImmutableDict doesn't allow changes")

    def update(self, *args, **kwargs):
        raise RuntimeError("ImmutableDict doesn't allow changes")
