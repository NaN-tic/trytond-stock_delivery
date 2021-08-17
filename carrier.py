# This file is part of the stock_delivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Carrier']


class Carrier(metaclass=PoolMeta):
    __name__ = 'carrier'
    tracking_ref_uri = fields.Char('URL Tracking Reference',
        help=('URI expression that will be evaluated. '
            'ex: https://domain.com?ref={reference}'))
