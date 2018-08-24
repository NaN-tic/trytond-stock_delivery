# This file is part stock_delivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['ShipmentOut']


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'
    carrier_tracking_ref = fields.Char("Carrier Tracking Ref", states={
        'readonly': Eval('state') == 'done',
        }, depends=['state'])
    number_packages = fields.Integer('Number of Packages', states={
        'readonly': Eval('state') == 'done',
        }, depends=['state'])

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        cls._error_messages.update({
                'tracking_ref_cancel': (
                    '"%(shipment)s" has a carrier tracking reference. '
                    'Please, contact to the carrier and cancel the shipment'),
                })
        # add carrier readonly when has a carrier tracking reference
        if cls.carrier.states.get('readonly'):
            cls.carrier.states['readonly'] |= Eval('carrier_tracking_ref')
        else:
            cls.carrier.states['readonly'] = Eval('carrier_tracking_ref')
        cls.carrier.depends.append('carrier_tracking_ref')

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

    @classmethod
    def cancel(cls, shipments):
        for shipment in shipments:
            if shipment.carrier_tracking_ref:
                cls.raise_user_warning('tracking_ref_cancel%s'
                        % shipment.id,
                    'tracking_ref_cancel', {
                        'shipment': shipment.rec_name,
                        })
        super(ShipmentOut, cls).cancel(shipments)
