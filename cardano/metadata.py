from decimal import Decimal
import operator

_MININT = -(2 ** 64 - 1)
_MAXINT = 2 ** 64 - 1


class Metadata(dict):
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
                    {"k": Metadata.serialize_value(v), "v": Metadata.serialize_value(v)}
                    for k, v in val.items()
                ]
            }
        # This should never happen
        raise RuntimeError(
            "Found unserializable value of {} (type {})".format(val, str(type(val)))
        )

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
            data[Metadata.TYPE_RESOLVERS[ktype](kval)] = Metadata.TYPE_RESOLVERS[vtype](
                vval
            )
        return data

    @staticmethod
    def deserialize(txdata):
        """
        Deserializes transaction metadata ``dict`` and returns :class:``Metadata`` instance.
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

    def tx_dict(self):
        return {str(k): Metadata.serialize_value(v) for k, v in self.items()}
