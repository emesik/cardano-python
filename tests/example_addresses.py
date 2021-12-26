# Taken from cardano-addresses commit 266fdbe20a56747efa29c0279982eb1fc9092fff


ICARUS_OK = [
    # BootstrapSpec.hs
    # specIcarus defaultPhrase "44H/1815H/0H/0/0" "764824073",
    "Ae2tdPwUPEYz6ExfbWubiXPB6daUuhJxikMEb4eXRp5oKZBKZwrbJ2k7EZe",
    # specIcarus defaultPhrase "44H/1815H/0H/0/1" "764824073",
    "Ae2tdPwUPEZCJUCuVgnysar8ZJeyKuhjXU35VNgKMMTcXWmS9zzYycmwKa4",
    # specIcarus defaultPhrase "44H/1815H/0H/0/2" "764824073",
    "Ae2tdPwUPEZFJtMH1m5HvsaQZrmgLcVcyuk5TxYtdRHZFo8yV7yEnnJyqTs",
    # specIcarus defaultPhrase "44H/1815H/0H/0/0" "mainnet",
    "Ae2tdPwUPEYz6ExfbWubiXPB6daUuhJxikMEb4eXRp5oKZBKZwrbJ2k7EZe",
    # specIcarus defaultPhrase "44H/1815H/0H/0/1" "mainnet",
    "Ae2tdPwUPEZCJUCuVgnysar8ZJeyKuhjXU35VNgKMMTcXWmS9zzYycmwKa4",
    # specIcarus defaultPhrase "44H/1815H/0H/0/2" "mainnet",
    "Ae2tdPwUPEZFJtMH1m5HvsaQZrmgLcVcyuk5TxYtdRHZFo8yV7yEnnJyqTs",
]

BYRON_OK = [
    # BootstrapSpec.hs
    # specByron defaultPhrase "0H/0H" "764824073",
    "DdzFFzCqrhsf6hiTYkK5gBAhVDwg3SiaHiEL9wZLYU3WqLUpx6DP5ZRJr4rtNRXbVNfk89FCHCDR365647os9AEJ8MKZNvG7UKTpythG",
    # specByron defaultPhrase "0H/1H" "764824073",
    "DdzFFzCqrhssdAorKQ7hGGPgNS3akoiuNG6YY7bb11hYrm1x716eakbz3yUppMS6X4t8WgM3Nx9CwjqZk3oNgm8s9yooJTs5AS7ptFT6",
    # specByron defaultPhrase "0H/2H" "764824073",
    "DdzFFzCqrht4YH5irxboFprowLYgJLddd2iCQt5mrVyQS5CZFMeZbQtzJsHf4a6YQhPPNxtqBVP3Drsy1tdjecqq1FK1m2oAR5J8EcVe",
    # specByron defaultPhrase "0H/0H" "mainnet",
    "DdzFFzCqrhsf6hiTYkK5gBAhVDwg3SiaHiEL9wZLYU3WqLUpx6DP5ZRJr4rtNRXbVNfk89FCHCDR365647os9AEJ8MKZNvG7UKTpythG",
    # specByron defaultPhrase "0H/1H" "mainnet",
    "DdzFFzCqrhssdAorKQ7hGGPgNS3akoiuNG6YY7bb11hYrm1x716eakbz3yUppMS6X4t8WgM3Nx9CwjqZk3oNgm8s9yooJTs5AS7ptFT6",
    # specByron defaultPhrase "0H/2H" "mainnet",
    "DdzFFzCqrht4YH5irxboFprowLYgJLddd2iCQt5mrVyQS5CZFMeZbQtzJsHf4a6YQhPPNxtqBVP3Drsy1tdjecqq1FK1m2oAR5J8EcVe",
    # InspectSpec.hs
    # specInspectAddress ["Byron", "none"] []
    #    "37btjrVyb4KEgoGCHJ7XFaJRLBRiVuvcrQWPpp4HeaxdTxhKwQjXHNKL43NhXaQNa862BmxSFXZFKqPqbxRc3kCUeTRMwjJevFeCKokBG7A7num5Wh",
    # specInspectAddress ["Byron", "address_index", "account_index"]
    "DdzFFzCqrht5csm2GKhnVrjzKpVHHQFNXUDhAFDyLWVY5w8ZsJRP2uhwZq2CEAVzDZXYXa4GvggqYEegQsdKAKikFfrrCoHheLH2Jskr",
]

ICARUS_ERR = [
    # InspectSpec.hs
    # specInspectAddress ["Icarus", "none"] []
    "Ae2tdPwUPEYz6ExfbWubiXPB6daUuhJxikMEb4eXRp5oKZBKZwrbJ2k7EZe",
    # specInspectInvalid "non-matching crc32" []
    "Ae2tdPwUPEZ5QJkfzoJgarugsX3rUVbTjg8nqTYmuy2c2msy5augpnm91ZR",
    # PointerSpec.hs
    # specMalformedAddress
    "Ae2tdPwUPEYz6ExfbWubiXPB6daUuhJxikMEb4eXRp5oKZBKZwrbJ2k7EZe",
]

BYRON_ERR = [
    # DelegationSpec.hs
    # specMalformedAddress
    "Ae2tdPwUPEYz6ExfbWubiXPB6daUuhJxikMEb4eXRp5oKZBKZwrbJ2k7EZe",
    # specMalformedAddress
    "DdzFFzCqrhsf6hiTYkK5gBAhVDwg3SiaHiEL9wZLYU3WqLUpx6DP5ZRJr4rtNRXbVNfk89FCHCDR365647os9AEJ8MKZNvG7UKTpythG",
    # InspectSpec.hs
    # specInspectAddress ["Byron", "none"] []
    "37btjrVyb4KEgoGCHJ7XFaJRLBRiVuvcrQWPpp4HeaxdTxhKwQjXHNKL43NhXaQNa862BmxSFXZFKqPqbxRc3kCUeTRMwjJevFeCKokBG7A7num5Wh",
    # specInspectAddress ["Byron", "address_index", "account_index"]
    "DdzFFzCqrht5csm2GKhnVrjzKpVHHQFNXUDhAFDyLWVY5w8ZsJRP2uhwZq2CEAVzDZXYXa4GvggqYEegQsdKAKikFfrrCoHheLH2Jskr",
    # PointerSpec.hs
    # specMalformedAddress
    "DdzFFzCqrhsf6hiTYkK5gBAhVDwg3SiaHiEL9wZLYU3WqLUpx6DP5ZRJr4rtNRXbVNfk89FCHCDR365647os9AEJ8MKZNvG7UKTpythG",
]

SHELLEY_ERR = [
    # DelegationSpec.hs
    # specInvalidAddress
    "addr1qdu5vlrf4xkxv2qpwngf6cjhtw542ayty80v8dyr49rf5ewvxwdrt70qlcpeeagscasafhffqsxy36t90ldv06wqrk2q5ggg4z",
    # specInvalidXPub
    "stake_xvk1qfqcf4tp4ensj5qypqs640rt06pe5x7v2eul00c7rakzzvsakw3caelfuh6cg6nrkdv9y2ctkeu",
    # InspectSpec.hs
    # -- 32-byte long script hash
    # specInspectInvalid "Unknown address type" []
    "stake17pshvetj09hxjcm9v9jxgunjv4ehxmr0d3hkcmmvdakx7mrgdp5xscfm7jc",
    # PointerSpec.hs
    # specInvalidAddress
    "addr1qdu5vlrf4xkxv2qpwngf6cjhtw542ayty80v8dyr49rf5ewvxwdrt70qlcpeeagscasafhffqsxy36t90ldv06wqrk2q5ggg4z",
    # RewardSpec.hs
    # FIXME: this one seems to be perfectly valid
    # specShelley defaultPhrase "1852H/1815H/0H/2/0" 0
    #    "stake_test1ura3dk68y6echdmfmnvm8mej8u5truwv8ufmv830w5a45tcsfhtt2",
    # specShelley defaultPhrase "1852H/1815H/0H/2/0" 3
    "stake1u0a3dk68y6echdmfmnvm8mej8u5truwv8ufmv830w5a45tchw5z0e",
]

GENERAL_ERR = [
    # DelegationSpec.hs
    # specMalformedAddress
    "💩",
    # specMalformedAddress
    "\0",
    # InspectSpec.hs
    # specInspectInvalid "Wrong input size of 28" []
    "79467c69a9ac66280174d09d62575ba955748b21dec3b483a9469a65",
]
