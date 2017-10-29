#!/usr/bin/env python3
import unittest

from my_country_codes import get_country_code

class CountryCodesTestCase(unittest.TestCase):
    """Tests for country_codes.py."""

    def test_get_country_code(self):
        country_code = get_country_code('Andorra')
        self.assertEqual(country_code, 'ad')

        country_code = get_country_code('United Arab Emirates')
        self.assertEqual(country_code, 'ae')

        country_code = get_country_code('Afghanistan')
        self.assertEqual(country_code, 'af')

        country_code = get_country_code('Venezuela, Bolivarian Republic of')
        self.assertEqual(country_code, 've')

unittest.main()