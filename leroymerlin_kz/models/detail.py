# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Detail(models.Model):
    
    _name = 'detail'
    _description = 'Detail'

    productnumber = fields.Char(string='Product ID')
    detail = fields.Char(string='Detail')
    value = fields.Char(string='Value')
