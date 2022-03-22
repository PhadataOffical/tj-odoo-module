from odoo import models, fields


class SaleOrderExtends(models.Model):
    _inherit = 'sale.order'

    tj_signed = fields.Boolean(string="已签名", readonly=True)
    tj_signed_by = fields.Many2one('res.users', string='签署人', readonly=True)
    tj_signed_id = fields.Many2one('sale.sign', string='签署内容', help='存储签署完成后的PDF的Base64编码', readonly=True)
    tj_signed_on = fields.Datetime('签署时间', help='Date of the signature', copy=False, readonly=True)
    tj_signed_status = fields.Selection([('none', '未签署'), ('signed', '已签署')],
                                        string='签署状态', default='none', readonly=True)
    tj_serial_number = fields.Char(string='CA证书序列号', readonly=True)
    # status = fields.Selection([('none', '未签署'), ('signed', '已签署')],string='签署状态', default='none', readonly=True)

    def action_pdf(self):
        data = {
            'order_id': self.id,
            'sign_id': self.tj_signed_id.id,
            'pdf_base64': self.tj_signed_id.content,
            'pdf_url': '/tj/sale-sign/sign/pdf/' + str(self.id),
        }
        return {
            'name': '签署文档',
            'type': 'ir.actions.client',
            'tag': 'sale.sign.pdf.page',
            'target': 'new',
            'params': data,
            'context': data
        }

    def action_sign(self):
        self.ensure_one()
        seals = self.env['tj.seal.manage'].search_read_seal()
        return {
            'type': 'ir.actions.client',
            'name': '电子签章',
            'tag': 'sale.sign.form.page',
            # 'target': 'new',
            'context': {
                'sale_order_id': self.id,
                'sale_order_model': self,
                'sale_order_pdf_url': '/report/pdf/sale.report_saleorder/' + str(self.id),
            },
            'params': {
                'seals': seals,
                'order_id': self.id,
                'pdf_url': '/tj/sale-sign/order/pdf/' + str(self.id),
                'html_url': '/tj/sale-sign/order/html/' + str(self.id),
            }
        }

