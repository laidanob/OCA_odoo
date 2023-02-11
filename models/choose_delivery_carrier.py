from odoo import fields, models

class ChooseDeliveryCarrierCost(models.TransientModel):
    _inherit = 'choose.delivery.carrier'
    
    cost = fields.Float()
    
    def _get_shipment_rate(self):
        vals = self.carrier_id.rate_shipment(self.order_id)
        if vals.get('success'):
            self.delivery_message = vals.get('warning_message', False)
            self.delivery_price = vals['price']
            self.display_price = vals['carrier_price']
            self.cost = vals['cost']
            
            return {}
        return {'error_message': vals['error_message']}
    
    def button_confirm(self):
        print('FUNCIONA')
        self.order_id.set_delivery_line(self.carrier_id, self.delivery_price,self.cost)
        self.order_id.write({
            'recompute_delivery_price': False,
            'delivery_message': self.delivery_message,
        })
   