# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LeroymerlinkzDetail(models.Model):
    
    _name = 'leroymerlinkz.detail'
    _description = 'Leroymerlin.kz Details'

    productnumber = fields.Char(string='Product ID')
    detail = fields.Char(string='Detail')
    value = fields.Char(string='Value')
