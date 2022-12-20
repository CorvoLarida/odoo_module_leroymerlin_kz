# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Product(models.Model):
    
    _name = 'product'
    _description = 'Product'
    
    productnumber = fields.Char(string='Product ID')
    name = fields.Char(string='Name')
    price = fields.Monetary(string='Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency',string='Currency')
    quantity = fields.Integer(string='Quantity')
    description = fields.Char(string='Description')
    specialorder = fields.Boolean(string='Is Special Order')

    _sql_constraints = [('productnumber_check', 'UNIQUE (productnumber)','Product ID must be unique.')]
    
