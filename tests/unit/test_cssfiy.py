# Copyright (c) 2025 Santiycr
#
# This file is part of Santiycr/cssify.
# Visit: https://github.com/santiycr/cssify

import os
import sys

from caqui.cssify import XpathException, cssify
from tests.unit.test_data import SUPPORTED, UNSUPPORTED

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import unittest


class CssifyTest(unittest.TestCase):
    def test_supported(self):
        for path, cssified in SUPPORTED:
            self.assertEqual(cssify(path), cssified)

    def test_unsupported(self):
        for path in UNSUPPORTED:
            self.assertRaises(XpathException, cssify, (path))
