#!/usr/bin/env python
# This file is part stock_delivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends


class StockDeliveryTestCase(unittest.TestCase):
    'Test Stock Delivery module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('stock_delivery')

    def test0005views(self):
        'Test views'
        test_view('stock_delivery')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockDeliveryTestCase))
    return suite
