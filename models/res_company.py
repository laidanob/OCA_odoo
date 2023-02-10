# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import requests
import xml.etree.ElementTree as ET

class ResCompany(models.Model):
    _inherit = 'res.company'

    codigoOrigen = fields.Char(string='Codigo postal Origen', help='Codigo postal de Origen, obligatorio')
    cuit = fields.Char(string='CUIT con "-"', help='CUIT. Obligatorio.')
    operativaSucursal = fields.Char(string='Contrato para envíos a sucursal', help='Número de Operativa para envíos a sucursal OCA. Obligatorio.')
    operativaDomicilio = fields.Char(string='Contrato para envíos estándar a domicilio', help='Número de Operativa para envíos a domicilio. Obligatorio.')
    operativaUrgenteDomicilio = fields.Char(string='Contrato para envíos urgentes a domicilio', help='Número de Operativa para envíos a domicilio de forma urgente. Obligatorio.')
    operativaUrgenteSucursal = fields.Char(string='Contrato para envíos urgentes a sucursal', help='Número de Operativa para envíos a sucursal de forma urgente. Obligatorio.')
    pesoDefecto = fields.Char(string='Peso en KG por defecto de todos los paquetes', help='Peso por defecto de todos los paquetes. Obligatorio.')
    volumenDefecto= fields.Char(string='Volumen por defecto de todos los paquetes ejemplo: 0,6', help='Volumen por defecto de todos los paquetes ejemplo: 0,6. Obligatorio.')
    cantidadPaquetes= fields.Char(string='Cantidad de Paquete por defecto', help='Cantidad de Paquete por defecto. Obligatorio.')
    cantidadProductos= fields.Integer(string='Cantidad de Productos para envio sin cargo', help='Cantidad de Paquete por defecto. Obligatorio.')


