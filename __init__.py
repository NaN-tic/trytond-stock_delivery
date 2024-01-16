# This file is part stock_delivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import carrier
from . import shipment


def register():
    Pool.register(
        shipment.ShipmentOut,
        module='stock_delivery', type_='model')
    Pool.register(
        carrier.Carrier,
        depends=['carrier'],
        module='stock_delivery', type_='model')
