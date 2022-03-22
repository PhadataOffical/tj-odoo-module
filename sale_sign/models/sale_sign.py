from odoo import models, fields, api


class SaleSign(models.Model):
    _name = 'sale.sign'

    name = fields.Char(string='名称', readonly=True)
    content = fields.Text(string='签署内容', readonly=True)  # PDF BASE64
    unique_code = fields.Char(string='用户唯一识别码', readonly=True)
    user_id = fields.Many2one('res.users', string='签署人', readonly=True)
    seal_id = fields.Many2one('tj.seal.manage', string='印章', readonly=True)
    order_id = fields.Many2one('sale.order', string='签署订单', help='签署的订单内容ID外健', readonly=True)
    status = fields.Selection([('none', '无效'), ('signing', '签署中'), ('signed', '已签署')],
                              string='签署状态', default='none', readonly=True)
    ident_no = fields.Char(string='企业性用代码', readonly=True)
    type = fields.Selection([('sale', '销售订单')], string='签署类型', default='sale', readonly=True)
    signed_on = fields.Datetime('签署时间', help='Date of the signature', copy=False, readonly=True)

    def action_pdf(self):
        data = {
            'sign_id': self.id,
            'order_id': self.order_id.id,
            'pdf_base64': self.content,
            'pdf_url': '/tj/sale-sign/sign/pdf/' + str(self.order_id.id),
        }
        return {
            'type': 'ir.actions.client',
            'name': '签署文档',
            'tag': 'sale.sign.pdf.page',
            'target': 'new',
            'params': data,
            'context': data
        }
