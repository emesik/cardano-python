from ...address import Address
from ...numbers import from_lovelaces, BlockPosition
from ...transaction import Input, Output


def get_amount(data):
    assert data["unit"] == "lovelace"
    return from_lovelaces(data["quantity"])


def get_block_position(data):
    return BlockPosition(
        data["epoch_number"], data["slot_number"], data["absolute_slot_number"]
    )


def get_input(data):
    return Input(
        iid=data["id"],
        address=Address(data["address"]),
        amount=get_amount(data["amount"]),
    )


def get_output(data):
    return Output(address=Address(data["address"]), amount=get_amount(data["amount"]))
