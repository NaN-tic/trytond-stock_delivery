# This file is part stock_delivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
from trytond.i18n import gettext
from trytond.exceptions import UserWarning

__all__ = ['ShipmentOut']


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'
    carrier_tracking_ref = fields.Char("Carrier Tracking Ref", states={
        'readonly': Eval('state') == 'done',
        }, depends=['state'])
    carrier_tracking_ref_uri = fields.Function(fields.Char(
        "Carrier Tracking Ref URI"), 'on_change_with_carrier_tracking_ref_uri')
    number_packages = fields.Integer('Number of Packages', states={
        'readonly': Eval('state') == 'done',
        }, depends=['state'])

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        if hasattr(cls, 'carrier'):
            # add carrier readonly when has a carrier tracking reference
            if cls.carrier.states.get('readonly'):
                cls.carrier.states['readonly'] |= Eval('carrier_tracking_ref')
            else:
                cls.carrier.states['readonly'] = Eval('carrier_tracking_ref')
            cls.carrier.depends.append('carrier_tracking_ref')
            cls.on_change_with_carrier_tracking_ref_uri.depends.add('carrier')

    @staticmethod
    def default_number_packages():
        return 1

    @fields.depends('carrier_tracking_ref')
    def on_change_with_carrier_tracking_ref_uri(self, name=None):
        if not hasattr(self, 'carrier'):
            return

        if (self.carrier and self.carrier.tracking_ref_uri
                and self.carrier_tracking_ref):
            return self.carrier.tracking_ref_uri.format(
                reference=self.carrier_tracking_ref)

    @classmethod
    def copy(cls, shipments, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['carrier_tracking_ref'] = None
        return super(ShipmentOut, cls).copy(shipments, default=default)

    @classmethod
    def cancel(cls, shipments):
        Warning = Pool().get('res.user.warning')
        for shipment in shipments:
            key = 'stock_delivery.tracking_ref_cancel_%d' % shipment.id
            if shipment.carrier_tracking_ref and Warning.check(key):
                raise UserWarning(key, gettext('stock_delivery.msg_tracking_ref_cancel',
                         shipment=shipment.rec_name))
        super(ShipmentOut, cls).cancel(shipments)
