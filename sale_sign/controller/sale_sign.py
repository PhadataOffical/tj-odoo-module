import datetime
import tempfile

from odoo import http
from odoo.http import request
from ..utils import minio
from ..network import cert_auth_api as ca_api
from contextlib import closing
import os
import base64
import tempfile

MINIO_USER = "admin"
MINIO_PASSWORD = "12345678"
# MINIO_URL = "192.168.1.101:9000"
# MINIO_URL = "minio.dev.tdaas.phadata.net"
# MINIO_URL = "files.dev.tdaas.phadata.net"
MINIO_URL = "oss.tdaas.dev.phadata.net"


class SaleSignController(http.Controller):

    @http.route('/count', type='json', auth='none')
    def count(self, **kwargs):
        return """
        <h1>HELLO Odoo</h1>
        """

    @http.route('/tj/sale-sign/order/sign/result', type='json', auth='user')
    def order_sign_result(self, order_id: int, result_id: str):
        result = ca_api.getSealSignResult(result_id)

        # result = {
        #     'code': '200000',
        #     'payload': {
        #         'data': 'asdfhgjhkjjghfgdfddwerhtfjgfnbdvscsdfgjnbarwetrytykujhmbvcxDfghfgjhmbnvcbxvc',
        #         'uniqueCode': 'sale_order_' + str(order_id)
        #     }
        # }

        if result['code'] == '200000':

            data_base64 = result['payload']['data']
            # uniqueCode = result['payload']['uniqueCode']

            # signs = request.env['sale.sign'].search([('unique_code', '=', uniqueCode)])
            signs = request.env['sale.sign'].search([('order_id', '=', int(order_id))])
            if signs:
                signs.write({
                    'content': data_base64,
                    'status': 'signed',
                    'signed_on': datetime.datetime.now()
                })

                seals = request.env['tj.seal.manage'].sudo().search([('id', '=', signs[0].seal_id.id)])
                order = request.env['sale.order'].sudo().search([('id', '=', signs[0].order_id.id or order_id)])
                if order:
                    order[0].write({
                        'tj_signed': True,
                        'tj_signed_id': signs[0].id,
                        'tj_signed_by': request.env.uid,
                        'tj_signed_on': datetime.datetime.now(),
                        'tj_signed_status': 'signed',
                        'tj_serial_number': seals[0].serialnumber,
                    })
        return result

    @http.route('/tj/sale-sign/order/sign', type='json', auth='user')
    def order_sign(self, order_id: int, seal_id: int, x: int, y: int, w: int, h: int, callBackUrl: str):
        context = dict(request.env.context)
        report = request.env['ir.actions.report']._get_report_from_name('sale.report_saleorder')
        pdf = report.with_context(context)._render_qweb_pdf([int(order_id)])[0]

        body_file_fd, pdf_file_path = tempfile.mkstemp(suffix='.html', prefix='report.pdf.')
        with closing(os.fdopen(body_file_fd, 'wb')) as body_file:
            body_file.write(pdf)

        bucket_name = "odoo.sale.sign.order.pdf"
        file_name = str(order_id) + ".pdf"
        minio_obj = minio.Bucket(service=MINIO_URL, access_key=MINIO_USER, secret_key=MINIO_PASSWORD, secure=True)
        minio_obj.create_bucket(bucket_name)
        minio_obj.fput_file(bucket_name, file_name, pdf_file_path)
        pdfUrl = minio_obj.presigned_get_file(bucket_name, file_name)

        # seal = request.env['tj.seal.manage'].browse(seal_id)
        # serialnumber = seal.serialnumber

        seals = request.env['tj.seal.manage'].sudo().search([('id', '=', seal_id)])
        serialnumber = seals[0].serialnumber

        uniqueCode = 'sale_order_' + str(order_id)  # 可以 NULL
        identNo = request.env.company.phadata_company_code  # 企業信用代碼
        # identNo = request.env.company.company_registry  # 企業信用代碼

        # uniqueCode = '1234567890-'

        order = request.env['sale.order'].browse(order_id)
        last_signs = request.env['sale.sign'].search([('unique_code', '=', uniqueCode)])

        if last_signs:
            last_signs.write({
                'name': order.name + ' - 签署',
                'order_id': order_id,
                'seal_id': seal_id,
                'user_id': request.env.uid,
                'ident_no': identNo,
                'unique_code': uniqueCode
            })
        else:
            request.env['sale.sign'].create({
                'name': order.name + ' - 签署',
                'ident_no': identNo,
                'seal_id': seal_id,
                'unique_code': uniqueCode,
                'status': 'signing',
                'type': 'sale',
                'order_id': order_id,
                'user_id': request.env.uid
            })

        # callBackUrl = ''
        # company = request.env['res.company'].browse(request.env.company.id)
        # identNo = company.company_registry  # 企業信用代碼
        # uniqueCode = request.env.company.company_registry

        # return {
        #     'pdfUrl': pdfUrl,
        #     'identNo': identNo,
        #     # 'uniqueCode': uniqueCode,
        #     'serialnumber': serialnumber
        # }
        return ca_api.sealSignature(x, y, w, h, pdfUrl, identNo, uniqueCode, serialnumber, callBackUrl)

    @http.route('/tj/sale-sign/order/html/<int:order_id>', type='http', auth='user')
    def order_html(self, order_id):
        context = dict(request.env.context)
        report = request.env['ir.actions.report']._get_report_from_name('sale.report_saleorder')
        html = report.with_context(context)._render_qweb_html([int(order_id)])[0]
        return request.make_response(html)


    @http.route('/tj/sale-sign/order/pdf/<int:order_id>', type='http', auth='user')
    def order_pdf(self, order_id):
        context = dict(request.env.context)
        report = request.env['ir.actions.report']._get_report_from_name('sale.report_saleorder')
        pdf = report.with_context(context)._render_qweb_pdf([int(order_id)])[0]
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf, headers=pdfhttpheaders)


    @http.route('/tj/sale-sign/sign/pdf/<int:order_id>', type='http', auth='user')
    def order_sigin_pdf(self, order_id: int):
        signs = request.env['sale.sign'].search([('order_id', '=', int(order_id)), ('status', '=', 'signed')])
        if signs:
            pdf = base64.b64decode(signs[0].content)
            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf)),
                ('Content-Disposition', 'inline; filename=' + signs[0].order_id.name + '-signed.pdf')
            ]
            return request.make_response(pdf, headers=pdfhttpheaders)
        return self.order_pdf(order_id)
