import re

PREFIXES = [
    "addr",
    "addr_test",
    "script",
    "stake",
    "stake_test"
    #      -- * Hashes
    ,
    "addr_vkh",
    "stake_vkh",
    "addr_shared_vkh",
    "stake_shared_vkh"
    #      -- * Keys for 1852H
    ,
    "addr_vk",
    "addr_sk",
    "addr_xvk",
    "addr_xsk",
    "acct_vk",
    "acct_sk",
    "acct_xvk",
    "acct_xsk",
    "root_vk",
    "root_sk",
    "root_xvk",
    "root_xsk",
    "stake_vk",
    "stake_sk",
    "stake_xvk",
    "stake_xsk"
    #      -- * Keys for 1854H
    ,
    "addr_shared_vk",
    "addr_shared_sk",
    "addr_shared_xvk",
    "addr_shared_xsk",
    "acct_shared_vk",
    "acct_shared_sk",
    "acct_shared_xvk",
    "acct_shared_xsk",
    "root_shared_vk",
    "root_shared_sk",
    "root_shared_xvk",
    "root_shared_xsk",
    "stake_shared_vk",
    "stake_shared_sk",
    "stake_shared_xvk",
    "stake_shared_xsk",
]

SHELLEY_ADDR_RE = re.compile("^(" + "|".join(PREFIXES) + ")")
