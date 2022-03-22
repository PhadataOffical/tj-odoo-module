from odoo import models, fields, api


class Cert(models.Model):
    """
    证书
    """
    _name = 'tj.cert'
    _description = '证书'

    # 	用户身份证/社会信用代码
    ident_no = fields.Char(string='用户身份证/社会信用代码', required=True)
    # 	签名证书序列号
    serialnumber = fields.Char(string='签名证书序列号', required=True)
    # 	证书内容的base64
    sign_cert = fields.Char(string='证书内容的base64', required=True)
    # 	用户唯一识别码
    unique_code = fields.Char(string='用户唯一识别码', required=True)
    # 	证书绑定的印模主键
    seal_id = fields.Integer(string='证书绑定的印模主键')
    # 	证书绑定印模后，ca审核的状态[0: 待审核  1:审核通过  2:审核不通过]
    status = fields.Integer(string='证书绑定印模后，ca审核的状态[0: 待审核  1:审核通过  2:审核不通过]')
    # 	审核状态原因
    reason = fields.Char(string='审核状态原因')
    # 	证书的申请时间
    apply_date = fields.Date(string='证书的申请时间')
    # 	申请证书返回的resultId，可以用来去贵州ca查询证书信息
    result_id = fields.Char(string='申请证书返回的resultId，可以用来去贵州ca查询证书信息')

    @api.model
    def create(self, vals_list):
        print(vals_list)
        result = super(Cert, self).create(vals_list)
        print(vals_list)
        return result
