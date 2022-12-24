# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LeroymerlinkzProduct(models.Model):
    
    _name = 'leroymerlinkz.product'
    _description = 'Leroymerlin.kz Products'
    
    productnumber = fields.Char(string='Product ID')
    name = fields.Char(string='Full Name')
    price = fields.Monetary(string='Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency')
    quantity = fields.Integer(string='Quantity')
    description = fields.Text(string='Description')
    specialorder = fields.Boolean(string='Is Special Order')

    _sql_constraints = [('productnumber_check', 'UNIQUE (productnumber)','Product ID must be unique.')]
    

    
