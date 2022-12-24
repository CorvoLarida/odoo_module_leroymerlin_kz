# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LeroymerlinkzCatalog(models.Model):
    
    _name = 'leroymerlinkz.catalog'
    _description = 'Leroymerlin.kz Catalog'
    
    productnumber = fields.Char(string='Product ID')
    categorylv1 = fields.Char(string='First Category')
    categorylv2 = fields.Char(string='Second Category')
    categorylv3 = fields.Char(string='Third Category')

    _sql_constraints = [('productnumber_check', 'UNIQUE (productnumber)','Product ID must be unique.')]
    
