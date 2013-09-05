#This file is part stock_delivery module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['ShipmentOut']
__metaclass__ = PoolMeta


class ShipmentOut:
    "Customer Shipment"
    __name__ = 'stock.shipment.out'
    carrier_tracking_ref = fields.Char("Carrier Tracking Ref")
    number_packages = fields.Integer('Number of Packages')

    @staticmethod
    def default_number_packages():
        return 1
