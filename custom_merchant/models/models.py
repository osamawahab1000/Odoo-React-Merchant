# -*- coding: utf-8 -*-

from odoo import models, fields, api
import uuid


class MerchantInfo(models.Model):
    _name = 'merchant.info'

    merchant_id = fields.Char('Merchant ID', required=True, copy=False, readonly=True,
                              default=lambda self: uuid.uuid4().hex)
    name = fields.Char('Merchant Name', required=True)
    business_type = fields.Char('Business Type', required=True)
    location = fields.Char('Location', required=True)
    email = fields.Char('Email', required=True)
    phone = fields.Char('Phone Number', required=True)
    payment_method = fields.Selection([
        ('mobile_money', 'Mobile Money'),
        ('bank', 'Bank'),
        ('cash', 'Cash')
    ], string='Preferred Payment Method', required=True)
    transaction_ids = fields.One2many('merchant.transaction', 'merchant_id', string="Transactions")

class MerchantTransaction(models.Model):
    _name = 'merchant.transaction'

    merchant_id = fields.Many2one('merchant.info', string="Merchant")
    transaction_date = fields.Datetime(string="Transaction Date", required=True)
    amount = fields.Float(string="Amount", required=True)
    payment_method = fields.Selection([
        ('money', 'Mobile Money'),
        ('bank', 'Bank'),
        ('cash', 'Cash'),
    ], string="Payment Method", required=True)