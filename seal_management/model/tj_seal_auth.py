from odoo import models, fields, api


class TJSealAuth(models.Model):
    _name = 'tj.seal.auth'
    _description = '印章授权中间表'
    seal_id = fields.Integer()
    user_id = fields.Integer()
