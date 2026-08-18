# This file is part stock_delivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Bool, Eval
from trytond.i18n import gettext
from trytond.exceptions import UserWarning

__all__ = ['ShipmentOut']


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    carrier_request_date = fields.Date('Carrier Request Date', states={
        'invisible': ~Bool(Eval('carrier')),
        'readonly': Eval('state') == 'done',
        })
    carrier_tracking_ref = fields.Char("Carrier Tracking Number", states={
        'readonly': Eval('state') == 'done',
        })
    carrier_tracking_url = fields.Function(fields.Char(
        'Carrier Tracking URL', readonly=True,
        states={
            'invisible': ~Bool(Eval('carrier')),
            }), 'on_change_with_carrier_tracking_url')
    number_packages = fields.Integer('Number of Packages', states={
        'readonly': Eval('state') == 'done',
        })

    @staticmethod
    def default_number_packages():
        return 1

    @fields.depends(
        'carrier', 'carrier_tracking_ref', 'company', 'warehouse',
        'delivery_address',
        '_parent_delivery_address.postal_code')
    def on_change_with_carrier_tracking_url(self, name=None):
        if not (self.carrier and self.carrier_tracking_ref):
            return
        api = next((a for a in self.carrier.apis
                if a.company == self.company and a.warehouse == self.warehouse),
            None)
        if not api:
            api = next((a for a in self.carrier.apis
                    if a.company == self.company and not a.warehouse), None)
        if not api:
            return
        url = api.render_url_tracking_ref(self)
        return url.decode() if isinstance(url, bytes) else url

    @classmethod
    def copy(cls, shipments, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['carrier_tracking_ref'] = None
        default['carrier_request_date'] = None
        return super().copy(shipments, default=default)

    @classmethod
    def cancel(cls, shipments):
        Warning = Pool().get('res.user.warning')
        for shipment in shipments:
            key = 'stock_delivery.tracking_ref_cancel_%d' % shipment.id
            if shipment.carrier_tracking_ref and Warning.check(key):
                raise UserWarning(key, gettext('stock_delivery.msg_tracking_ref_cancel',
                         shipment=shipment.rec_name))
        super().cancel(shipments)
