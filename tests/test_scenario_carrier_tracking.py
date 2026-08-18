from trytond.modules.carrier.tests.test_module import create_carrier
from trytond.modules.company.tests import create_company, set_company
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction


class TestCarrierTracking(ModuleTestCase):
    module = 'stock_delivery'

    @with_transaction()
    def test(self):
        pool = Pool()
        Address = pool.get('party.address')
        Api = pool.get('carrier.api')
        Location = pool.get('stock.location')
        Shipment = pool.get('stock.shipment.out')

        company = create_company()
        with set_company(company):
            carrier = create_carrier()
            address = Address(party=carrier.party, street='Test street',
                city='Barcelona', postal_code='08001')
            address.save()
            warehouse, = Location.search([('type', '=', 'warehouse')],
                limit=1)
            api = Api(company=company, warehouse=warehouse,
                url_tracking_ref=(
                    'https://mygls.gls-spain.es/e/'
                    '${record.carrier_tracking_ref}/'
                    '${record.delivery_address.postal_code}/es'))
            carrier.apis = [api]
            shipment = Shipment(company=company, warehouse=warehouse,
                carrier=carrier, delivery_address=address,
                carrier_tracking_ref='GLS123')

            self.assertEqual(shipment.on_change_with_carrier_tracking_url(),
                'https://mygls.gls-spain.es/e/GLS123/08001/es')


del ModuleTestCase
