Addresses
=========

At the moment the module doesn't have validation of Cardano addresses, other than checking if the
prefix is correct. It recognizes the following:

* Shelley era ``addr1`` and ``addr_test1``
* Byron era ``Ae2`` and ``DdzFF``

Addresses are instances of :class:`Address <cardano.address.Address>` class but you may use strings
instead. Conversion and comparison methods are provided. No other functionality is available yet.

Retrieving wallet addresses
---------------------------

To get a list of addresses available in a wallet, do the following:

.. code-block:: python

    In [6]: wal.addresses()
    Out[6]: [addr_test1qr9ujxmsvdya6r4e9lxlu4n37svn52us7z8uzqdkhw8muqld56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqzuzvzt,
            addr_test1qpjqfw0xn8wp3rt9633ja6ua2nfmpx70qdn67cutc93p02hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqvy6c2z,
            addr_test1qqaaeru7xswhg9n9653ajpcryxl0334ryfp3kpuvd6aw0hhd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqukuem0,
            addr_test1qqmv6m3mjwk8xfwc6mmxrah5fgrvvvtk0ncey84jcs4a798d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqzn97h7,
            addr_test1qznf0k97a9wn50yy3aw6l2zfugknczj45gyfk2nykk49qy0d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq88sus6,
            addr_test1qrkm3tgk74edkv60uqwedayw4kut0zgg5qgtm3epjvyxvt0d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqwu2s5h,
            addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e,
            addr_test1qrjvywxnrwv7ehx7f0enyta2n2lpjfk096df3mul9zr8vw8d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq737ksu,
            addr_test1qzyhv3csdwlyuwt7kgjvkjpfrq0ap3d6lpm0ej88yf6zuj8d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqfltagt,
            addr_test1qpzwtycspdltafh34fedqayuh755uefuafvnveta6tt95z8d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqk2emsk,
            addr_test1qqfkfcpcdd0ll44qj3wasnl6vdyay3zur7lpay4p49pxjt8d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqghlcdr,
            addr_test1qpd78m0427l4q62s305c0487gnqla07t33sdm9wenvgw23hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqcrzdqy,
            addr_test1qz3d7yap080hnkz8wjrmcng0euc5qamrl4s6daw0f8gwknld56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq8eeq7q,
            addr_test1qzunys8wvg5ssh2m6jrpvsckmjye30d7kzavrmq3gwkt270d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq85qdpf,
            addr_test1qqdvqczhy05zjsspaeaay3a27xey0lm2lwevl27sgfy4y88d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq6luvc6,
            addr_test1qqu76rcvmt5e86dyxv90dpch5adgafhdmy20hs36n07ds9hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgq0nyj,
            addr_test1qp00p2y2yf9gkqul9w0jzfyju690flpefunjdl7z9cm2wdld56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq0aw9al,
            addr_test1qzkh6wkkhgf57g5s6tqpt342fqezurx7tmapdw8q3mlud2hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqnr9zdq,
            addr_test1qr9y5q90w2e866gc5ehs5h2dqwzdd9maenpxf6wdj4c5238d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqspuwcy,
            addr_test1qzhjjeqt42lc0g48mlljsjxlleu24q206vxgtd7fu3vrzyhd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqv5nvpg]

Optionally, you may also retrieve info whether each of the addresses has been used. That means, it
has received some funds. Please note the returned structure will be now a list of tuples
``(address, used)``.

.. code-block:: python

    In [7]: wal.addresses(with_usage=True)
    Out[7]: [(addr_test1qr9ujxmsvdya6r4e9lxlu4n37svn52us7z8uzqdkhw8muqld56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqzuzvzt, True),
            (addr_test1qp64xq7fsz9kvjwjy5tzfpetp2jmmhhk68kw066wqvyfgvhd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqj7msh0, True),
            (addr_test1qpjqfw0xn8wp3rt9633ja6ua2nfmpx70qdn67cutc93p02hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqvy6c2z, False),
            (addr_test1qqaaeru7xswhg9n9653ajpcryxl0334ryfp3kpuvd6aw0hhd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqukuem0, False),
            (addr_test1qqmv6m3mjwk8xfwc6mmxrah5fgrvvvtk0ncey84jcs4a798d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqzn97h7, False),
            (addr_test1qznf0k97a9wn50yy3aw6l2zfugknczj45gyfk2nykk49qy0d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq88sus6, False),
            (addr_test1qrkm3tgk74edkv60uqwedayw4kut0zgg5qgtm3epjvyxvt0d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqwu2s5h, False),
            (addr_test1qqd86dlwasc5kwe39m0qvu4v6krd24qek0g9pv9f2kq9x28d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgepa9e, False),
            (addr_test1qrjvywxnrwv7ehx7f0enyta2n2lpjfk096df3mul9zr8vw8d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq737ksu, False),
            (addr_test1qzyhv3csdwlyuwt7kgjvkjpfrq0ap3d6lpm0ej88yf6zuj8d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqfltagt, False),
            (addr_test1qpzwtycspdltafh34fedqayuh755uefuafvnveta6tt95z8d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqk2emsk, False),
            (addr_test1qqfkfcpcdd0ll44qj3wasnl6vdyay3zur7lpay4p49pxjt8d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqghlcdr, False),
            (addr_test1qpd78m0427l4q62s305c0487gnqla07t33sdm9wenvgw23hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqcrzdqy, False),
            (addr_test1qz3d7yap080hnkz8wjrmcng0euc5qamrl4s6daw0f8gwknld56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq8eeq7q, False),
            (addr_test1qzunys8wvg5ssh2m6jrpvsckmjye30d7kzavrmq3gwkt270d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq85qdpf, False),
            (addr_test1qqdvqczhy05zjsspaeaay3a27xey0lm2lwevl27sgfy4y88d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq6luvc6, False),
            (addr_test1qqu76rcvmt5e86dyxv90dpch5adgafhdmy20hs36n07ds9hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqgq0nyj, False),
            (addr_test1qp00p2y2yf9gkqul9w0jzfyju690flpefunjdl7z9cm2wdld56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswq0aw9al, False),
            (addr_test1qzkh6wkkhgf57g5s6tqpt342fqezurx7tmapdw8q3mlud2hd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqnr9zdq, False),
            (addr_test1qr9y5q90w2e866gc5ehs5h2dqwzdd9maenpxf6wdj4c5238d56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqspuwcy, False),
            (addr_test1qzhjjeqt42lc0g48mlljsjxlleu24q206vxgtd7fu3vrzyhd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqv5nvpg, False),
            (addr_test1qzhhm8em4pundp2ypcd36euplhe39pmuah290meu6l6gtqhd56vd3zqzthdaweyrktfm3h5cz4je9h5j6s0f24pryswqusvkfl, False)]

API reference
-------------

.. automodule:: cardano.address
   :members:
