# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests,urllib
import xml.etree.ElementTree as ET


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[
                                                    ('ocaSucursal', 'OCA Sucursal'),
                                                    ('ocaDomicilio', 'OCA Domicilio'),
                                                    ('ocaPrioritarioSucursal', 'OCA Prioritario Sucursal'),
                                                    ('ocaPrioritarioDomicilio', 'OCA Prioritario Domicilio')
                                                    ],
                                                    ondelete={'ocaSucursal': 'set default',
                                                            'ocaDomicilio': 'set default',
                                                            'ocaPrioritarioSucursal': 'set default',
                                                            'ocaPrioritarioDomicilio': 'set default'}
                                                    )
    
    urlRateShipment = 'http://webservice.oca.com.ar/oep_tracking/Oep_Track.asmx/Tarifar_Envio_Corporativo'

    cantidad= 0
    
    categorias = ["Premium", "Basic", "Nature", "Classic"]
    
    def _validacion_codigos(self,cp_cliente,cp_origen):
            if cp_cliente == False:
                raise ValidationError('¡El Cliente debe tener código postal!')
            if cp_origen == False:
                raise ValidationError('¡No hay codigo postal de origen!')
            
    def _conteo_productos(self,order):
        cantidad = self.cantidad
        categorias = self.categorias
        for line in order.order_line:
            diseno = line.product_id.name
            if diseno == "Diseño":
                pass
            elif line.product_id.public_categ_ids.name in categorias:
                cantidad += line.product_uom_qty
            return cantidad

    def _request_oca(self,operativa,order):
            cp_cliente = order.partner_shipping_id.zip
            cp_origen = order.company_id.codigoOrigen
            peso_defecto = order.company_id.pesoDefecto
            volumen_defecto = order.company_id.volumenDefecto
            cantidad_paquetes = order.company_id.cantidadPaquetes
            cuit = order.company_id.cuit
            
            self._validacion_codigos(cp_origen,cp_cliente)
     
            
            #la operativa es lo que define el tipo de envio en OCA, a domicilio, sucurcursal, prioritario, etc.

            params = {
                        "PesoTotal": peso_defecto,
                        "VolumenTotal": volumen_defecto,
                        "CodigoPostalOrigen": cp_origen,
                        "CodigoPostalDestino": cp_cliente,
                        "CantidadPaquetes": cantidad_paquetes,
                        "Cuit": cuit,
                        "Operativa": operativa
                        }

            url = self.urlRateShipment + "?" + urllib.parse.urlencode(params)
            
            r = requests.get(url)
            if r.status_code == 200:
                data = r.content
                tree = ET.fromstring(data)
                for i in tree.iter("Table"):
                    price = float(i.find("Total").text)
                    return price
                
            elif r.status_code == 401:
                return {
                    'success': False,
                    'price': 0,
                    'error_message': 'Error de autorización, revise sus credenciales.',
                    'warning_message': False
                }
            elif r.status_code == 408:
                return {
                    'success': False,
                    'price': 0.0,
                    'error_message': 'Error. La solicitud está tomando demasiado tiempo en procesarse, intente nuevamente.',
                    'warning_message': False
                }
            elif r.status_code == 500:
                return {
                    'success': False,
                    'price': 0,
                    'error_message': 'Error interno. Intente nuevamente. Revise su Codigo Postal',
                    'warning_message': False
                }
            elif r.status_code == 503:
                return {
                    'success': False,
                    'price': 0,
                    'error_message': 'Error interno. El servidor se encuentra saturado, espere unos minutos y vuelva a intentarlo.',
                    'warning_message': False
                }
            else:
                
                return {
                    'success': False,
                    'price': 0,
                    'error_message': 'Algo salió mal esta. Error n° ' + str(r.status_code) + url,
                    'warning_message': False
                }
              
    def ocaSucursal_rate_shipment(self, order):
        operativa = order.company_id.operativaSucursal
        price = self._request_oca(operativa,order)
        cantidad = self._conteo_productos(order)
        cantidad_productos = order.company_id.cantidadProductos
        if type(price) == dict:
            return price
        
        elif type(price) == int or type(price) == float:
            if cantidad_productos <= cantidad:
                return {
                    'success': True,
                    'price': 0,
                    'cost':price,
                    'error_message': False,
                    'warning_message': (f"Sin cargo porque tiene mas de tres libros, el valor seria {price}")
                    }
            else:
                return {
                    'success': True,
                    'price': price,
                    'cost': price,
                    'error_message': False,
                    'warning_message': (f'Para que el envio sea sin cargo tienes que agregar {int(order.company_id.cantidadProductos - cantidad)} fotolibros mas a tu compra')
                    }
     
    def ocaDomicilio_rate_shipment(self, order):
        operativa = order.company_id.operativaDomicilio
        price = self._request_oca(operativa,order)
        cantidad = self._conteo_productos(order)
        cantidad_productos = order.company_id.cantidadProductos
        if type(price) == dict:
            return price
        
        elif type(price) == int or type(price) == float:
            if cantidad_productos <= cantidad:
                return {
                    'success': True,
                    'price': 0,
                    'cost':price,
                    'error_message': False,
                    'warning_message': (f"Sin cargo porque tiene mas de tres libros, el valor seria {price}")
                    }
            else:
                return {
                    'success': True,
                    'price': price,
                    'cost': price,
                    'error_message': False,
                    'warning_message': (f'Para que el envio sea sin cargo tienes que agregar {int(order.company_id.cantidadProductos - cantidad)} fotolibros mas a tu compra')
                    }
    def ocaPrioritarioSucursal_rate_shipment(self, order):
        operativa = order.company_id.operativaUrgenteSucursal
        price = self._request_oca(operativa,order)
        cantidad = self._conteo_productos(order)
        cantidad_productos = order.company_id.cantidadProductos
        if type(price) == dict:
            return price
        
        elif type(price) == int or type(price) == float:
            if cantidad_productos <= cantidad:
                return {
                    'success': True,
                    'price': price,
                    'cost':price,
                    'error_message': False,
                    'warning_message': ("Los envios priopitarios no son sin cargo, como tenes 3 fotolibros, podes seleccionar otra opcion")
                    }
            else:
                return {
                    'success': True,
                    'price': price,
                    'cost': price,
                    'error_message': False,
                    'warning_message': False
                    }
        
    def ocaPrioritarioDomicilio_rate_shipment(self, order):
        operativa = order.company_id.operativaUrgenteDomicilio
        price = self._request_oca(operativa,order)
        cantidad = self._conteo_productos(order)
        cantidad_productos = order.company_id.cantidadProductos
        if type(price) == dict:
            return price
        
        elif type(price) == int or type(price) == float:
            if cantidad_productos <= cantidad:
                return {
                    'success': True,
                    'price': price,
                    'cost':price,
                    'error_message': False,
                    'warning_message': ("Los envios priopitarios no son sin cargo, como tenes 3 fotolibros, podes seleccionar otra opcion")
                    }
            else:
                return {
                    'success': True,
                    'price': price,
                    'cost': price,
                    'error_message': False,
                    'warning_message': False
                    }
    
    def ocaSucursal_send_shipping(self,pickings):
        print('221 oca module delivery carrier, pickings',pickings.browse())
        
        dic = [{
            'tracking_number': '12232',
            'exact_price': 0,
        }]
        return dic