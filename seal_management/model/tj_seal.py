import re

from odoo import models, fields, api


class TJSealMange(models.Model):
    _name = "tj.seal.manage"
    _description = 'TJ印章'
    # 印章名称
    seal_name = fields.Char(string='印章名称')
    seal_model_url = fields.Char(string='印章')
    seal_company_dtid = fields.Char(string='DTID')
    seal_company_name = fields.Selection(string='公司', selection='_companyName')
    seal_type_name = fields.Selection(
        [("公章", '公章'), ("合同专用章", '合同专用章'),
         ('法定代表人章', '法定代表人章'),
         ('财务专用章', '财务专用章'),
         ('通用印章', '通用印章')], string='印章类型')
    serialnumber = fields.Char(string='证书序列号')
    """"
            印模的可用状态
            0: 不可用
            1: 待审核
            2: 审核通过
            3: 审核不通过
    """
    status = fields.Integer(string='状态', default=0)
    """
         审核状态原因
    """
    reason = fields.Char(string='审核原因')

    seal_image = fields.Binary(string='印模上传')

    seal_image_name = fields.Char(string='印模名称')

    # attachment_number = fields.Integer(compute='_compute_attachment_number', string='印模上传')

    # seal_image_attachment = fields.Many2one('ir.attachment', string=u'印模上传')
    # seal_image_test = fields.Binary(u'测试')

    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'tj_seal_manage'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)

    def action_get_attachment_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'tj_seal_manage'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'tj_seal_manage', 'default_res_id': self.id}
        return re

    @api.model
    def create(self, vals):
        print(vals)
        res = super(TJSealMange, self).create(vals)
        return res

    #    self.env[attachment.res_model].browse(attachment.res_id)
    def mysearch(self, args, offset=0, limit=None, order=None, count=False):
        return

    def search_read_seal(self):
        """
        印章列表
        """
        records = self.search([('status', '=', '2')], offset=0, limit=None, order=None)
        # records = self.search([], offset=0, limit=None, order=None)
        if not records:
            return []
        result = records.read()
        print(self.env.user.read())
        if self.env.is_admin():
            # 返回所有
            index = {vals['id']: vals for vals in result}
            all = [index[record.id] for record in records if record.id in index]
            print(all)
            return all
        # 查询当前用户的印章授权列表
        sealAuth = self.env['tj.seal.auth'].sudo().search([('user_id', '=', self.env.user.id)])
        sa_ids = sealAuth.ids
        if len(sa_ids) <= 0:
            return []
        sa_data = sealAuth.read()
        resultData = []
        for item in result:
            for sa in sa_data:
                # 判断当前将当前用户拥有授权的印章数据返回
                if item['id'] == sa['seal_id']:
                    resultData.append(item)
        return resultData

    """
    附件上传参考
    https://www.cnblogs.com/ljwtiey/p/7348291.html
    https://blog.csdn.net/weixin_44611400/article/details/86647134
    """

    def attachment_image_preview(self):
        """附件上传 第二种方式"""
        self.ensure_one()
        # domain可以过滤指定的附件类型 （mimetype）
        domain = [('res_model', '=', self._name), ('res_id', '=', self.id)]
        return {
            'domain': domain,
            'res_model': 'ir.attachment',
            'name': '附件管理',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'limit': 20,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

    def _companyName(self):
        res = self.env['res.company'].search([])
        selection = [(company.name, company.name) for company in res]
        return selection
