#This file is part stock_delivery module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['ShipmentOut']


class ShipmentOut:
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.out'
    carrier_tracking_ref = fields.Char("Carrier Tracking Ref", states={
            'readonly': ~Eval('state').in_(['draft', 'waiting', 'assigned',
                    'packed']),
            }, depends=['state'])
    number_packages = fields.Integer('Number of Packages', states={
            'readonly': ~Eval('state').in_(['draft', 'waiting', 'assigned',
                    'packed']),
            }, depends=['state'])

    @staticmethod
    def default_number_packages():
        return 1

    @classmethod
    def copy(cls, shipments, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['carrier_tracking_ref'] = None
        return super(ShipmentOut, cls).copy(shipments, default=default)
