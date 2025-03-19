import json
from odoo import http
from odoo.http import request, Response

class MerchantAPI(http.Controller):

    def cors_headers(self, response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    @http.route('/api/merchant/create', type='json', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
    def create_merchant(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return self.cors_headers(Response())

        required_fields = ['name', 'business_type', 'location', 'email', 'phone', 'payment_method']
        missing_fields = [field for field in required_fields if field not in kwargs]
        if missing_fields:
            return self.cors_headers(Response(json.dumps({'success': False, 'error': f'Missing fields: {", ".join(missing_fields)}'}), status=400, mimetype="application/json"))

        merchant = request.env['merchant.info'].sudo().create({
            'name': kwargs['name'],
            'business_type': kwargs['business_type'],
            'location': kwargs['location'],
            'email': kwargs['email'],
            'phone': kwargs['phone'],
            'payment_method': kwargs['payment_method']
        })

        picking_type = request.env['stock.picking.type'].sudo().search([('code', '=', 'outgoing')], limit=1)
        payment_method = request.env['account.journal'].sudo().search([('type', '=', 'cash')], limit=1)

        request.env['pos.config'].sudo().create({
            'name': merchant.name,
            'picking_type_id': picking_type.id,
            'journal_id': payment_method.id,
        })

        return self.cors_headers(Response(json.dumps({'success': True, 'merchant_id': merchant.merchant_id}), status=200, mimetype="application/json"))

    @http.route('/api/merchant/<string:merchant_id>', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    def get_merchant(self, merchant_id):
        if request.httprequest.method == "OPTIONS":
            return self.cors_headers(Response())

        merchant = request.env['merchant.info'].sudo().search([('merchant_id', '=', merchant_id)], limit=1)
        if not merchant:
            return self.cors_headers(Response(json.dumps({'success': False, 'error': 'Merchant not found'}), status=404, mimetype="application/json"))

        response_data = {
            'success': True,
            'merchant': {
                'merchant_id': merchant.merchant_id,
                'name': merchant.name,
                'business_type': merchant.business_type,
                'location': merchant.location,
                'email': merchant.email,
                'phone': merchant.phone,
                'payment_method': merchant.payment_method
            }
        }
        return self.cors_headers(Response(json.dumps(response_data), status=200, mimetype="application/json"))

    @http.route('/api/merchant/transactions', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    def get_transactions(self, merchant_id):
        if request.httprequest.method == "OPTIONS":
            return self.cors_headers(Response())

        transactions = [
            {'transaction_id': 'TXN001', 'date': '2025-03-19', 'amount': 100, 'status': 'Completed', 'payment_method': 'Bank'},
            {'transaction_id': 'TXN002', 'date': '2025-03-18', 'amount': 200, 'status': 'Pending', 'payment_method': 'Mobile Money'}
        ]

        return self.cors_headers(Response(json.dumps({'success': True, 'transactions': transactions}), status=200, mimetype="application/json"))
