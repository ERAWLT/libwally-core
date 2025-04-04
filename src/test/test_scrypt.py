import os
import unittest
from util import *

# Test cases from
# https://tools.ietf.org/html/draft-josefsson-scrypt-kdf-04
cases = [
    ["", "",
     16, 1, 1, 64,
     '77 d6 57 62 38 65 7b 20 3b 19 ca 42 c1 8a 04 97'
     'f1 6b 48 44 e3 07 4a e8 df df fa 3f ed e2 14 42'
     'fc d0 06 9d ed 09 48 f8 32 6a 75 3a 0f c8 1f 17'
     'e8 d3 e0 fb 2e 0d 36 28 cf 35 e2 0c 38 d1 89 06'],

    ['password', 'NaCl',
     1024, 8, 16, 64,
     'fd ba be 1c 9d 34 72 00 78 56 e7 19 0d 01 e9 fe'
     '7c 6a d7 cb c8 23 78 30 e7 73 76 63 4b 37 31 62'
     '2e af 30 d9 2e 22 a3 88 6f f1 09 27 9d 98 30 da'
     'c7 27 af b9 4a 83 ee 6d 83 60 cb df a2 cc 06 40'],

    ['pleaseletmein', 'SodiumChloride',
     16384, 8, 1, 64,
     '70 23 bd cb 3a fd 73 48 46 1c 06 cd 81 fd 38 eb'
     'fd a8 fb ba 90 4f 8e 3e a9 b5 43 f6 54 5d a1 f2'
     'd5 43 29 55 61 3f 0f cf 62 d4 97 05 24 2a 9a f9'
     'e6 1e 85 dc 0d 65 1e 40 df cf 01 7b 45 57 58 87'],

    ['pleaseletmein', 'SodiumChloride',
     1048576, 8, 1, 64,
     '21 01 cb 9b 6a 51 1a ae ad db be 09 cf 70 f8 81'
     'ec 56 8d 57 4a 2f fd 4d ab e5 ee 98 20 ad aa 47'
     '8e 56 fd 8f 4b a5 d0 9f fa 1c 6d 92 7c 40 f4 c3'
     '37 30 40 49 e8 a9 52 fb cb f4 5c 6f a7 7a 41 a4']
]

class ScryptTests(unittest.TestCase):

    def test_scrypt(self):

        if os.getenv('WALLY_SKIP_EXPENSIVE_TESTS', None):
            self.skipTest('Skipping expensive scrypt test')

        # Invalid arguments
        pwd, salt, cost, block, p, l, _ = cases[0]
        pwd, salt = utf8(pwd), utf8(salt)
        out_buf, out_len = make_cbuffer('0' * l)
        invalid = [
            [pwd, len(pwd), salt, len(salt), cost, block, p, None,    out_len], # Null output
            [pwd, len(pwd), salt, len(salt), cost, block, p, out_buf, 0],       # Empty output
            [pwd, len(pwd), salt, len(salt), cost, block, p, out_buf, 33],      # Len not % 32
        ]
        for c in invalid:
            ret = wally_scrypt(*c)
            self.assertEqual(wally_scrypt(*c), WALLY_EINVAL)

        # Test vectors
        for c in cases:
            pwd, salt, cost, block, parallel, length, expected = c
            pwd = utf8(pwd)
            salt = utf8(salt)
            expected = expected.replace(' ', '')
            assert len(expected) == length * 2
            out_buf, out_len = make_cbuffer('0' * len(expected))

            ret = wally_scrypt(pwd, len(pwd), salt, len(salt),
                               cost, block, parallel, out_buf, out_len)
            self.assertEqual(ret, WALLY_OK)
            self.assertEqual(h(out_buf), utf8(expected))


if __name__ == '__main__':
    unittest.main()
