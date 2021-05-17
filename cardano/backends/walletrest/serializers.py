from dateutil.parser import isoparse
from decimal import Decimal
from ...address import Address
from ...numbers import from_lovelaces, to_lovelaces
from ...simpletypes import BlockPosition, Epoch
from ...transaction import Input, Output


def get_amount(data):
    assert data["unit"] == "lovelace"
    return from_lovelaces(data["quantity"])


def store_amount(amount):
    return {"quantity": to_lovelaces(amount), "unit": "lovelace"}


def get_percent(data):
    assert data["unit"] == "percent"
    return Decimal(data["quantity"]) / Decimal(100)


def get_block_position(data):
    return BlockPosition(
        data["epoch_number"], data["slot_number"], data["absolute_slot_number"]
    )


def get_stakingstatus(val):
    if val == "delegating":
        return True
    if val == "not_delegating":
        return False
    raise ValueError("Encountered invalid staking status: {}".format(val))


def get_epoch(data):
    return Epoch(data["epoch_number"], isoparse(data["epoch_start_time"]))


def get_input(data):
    return Input(
        iid=data["id"],
        address=Address(data["address"]) if "address" in data else None,
        amount=get_amount(data["amount"]) if "amount" in data else None,
    )


def get_output(data):
    return Output(address=Address(data["address"]), amount=get_amount(data["amount"]))


def store_interval(seconds):
    return {"quantity": int(seconds), "unit": "second"}
