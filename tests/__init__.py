# This file is part stock_delivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.stock_delivery.tests.test_stock_delivery import suite
except ImportError:
    from .test_stock_delivery import suite

__all__ = ['suite']
