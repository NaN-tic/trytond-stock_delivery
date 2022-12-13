# This file is part stock_delivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
from trytond.i18n import gettext
from trytond.exceptions import UserWarning


class StockDeliveryMixin(ModelSQL, ModelView):
    carrier_tracking_ref = fields.Char("Carrier Tracking Ref", states={
        'readonly': Eval('state') == 'done',
        }, depends=['state'])
    number_packages = fields.Integer('Number of Packages', states={
        'readonly': Eval('state') == 'done',
        }, depends=['state'])

    @staticmethod
    def default_number_packages():
        return 1

    @classmethod
    def __setup__(cls):
        super(StockDeliveryMixin, cls).__setup__()
        if hasattr(cls, 'carrier'):
            # add carrier readonly when has a carrier tracking reference
            if cls.carrier.states.get('readonly'):
                cls.carrier.states['readonly'] |= Eval('carrier_tracking_ref')
            else:
                cls.carrier.states['readonly'] = Eval('carrier_tracking_ref')
            cls.carrier.depends.add('carrier_tracking_ref')

    @classmethod
    def copy(cls, shipments, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['carrier_tracking_ref'] = None
        return super(StockDeliveryMixin, cls).copy(shipments, default=default)

    @classmethod
    def cancel(cls, shipments):
        Warning = Pool().get('res.user.warning')
        for shipment in shipments:
            key = 'stock_delivery.tracking_ref_cancel_%d' % shipment.id
            if shipment.carrier_tracking_ref and Warning.check(key):
                raise UserWarning(key, gettext('stock_delivery.msg_tracking_ref_cancel',
                         shipment=shipment.rec_name))
        super(StockDeliveryMixin, cls).cancel(shipments)


class ShipmentOut(StockDeliveryMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'


class ShipmentOutReturn(StockDeliveryMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.return'
