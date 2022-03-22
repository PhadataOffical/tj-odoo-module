# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..util import dtid_core


class PhadataDtidModel(models.Model):
    _inherit = 'res.users'
    _description = 'phadata_dtid_model'

    phadata_dtid = fields.Char()
    phadata_user_name = fields.Char()
    phadata_user_idNo = fields.Char()

    @api.model
    def get_dtid(self):
        data = {
            'account': self.env.user.login,
            'dtid': self.env.user.phadata_dtid,
            'username': self.env.user.phadata_user_name,
            'phone': self.env.company.phone,
            'company_name': self.env.company.phadata_company_name,
            'company_code': self.env.company.phadata_company_code,
            'license_b64': self.env.company.phadata_company_license_b64
        }
        return data

    @api.model
    def update_dtid(self, company_data, is_admin):
        # create dtid
        if is_admin:
            registry_resp = dtid_core.registry_dtid()
            try:
                if registry_resp is None:
                    raise Exception("Registry dtid error.")
                dtidDocument = registry_resp['dtidDocument']
                dtid = dtidDocument['id']
                # bind dtid
                bind_resp = dtid_core.bind_company_dtid(dtid_document=dtidDocument, company_data=company_data)
                if bind_resp is None:
                    raise Exception("Bind dtid error.")

                # update company data
                self.env['res.company'].update_company(company_data, dtid)
                # update user data
                self.env.user.write({
                    'phadata_user_name': company_data['name'],
                    'phadata_dtid': dtid
                })
            except Exception as ex:
                raise Exception(ex)
        else:
            # update data
            if company_data:
                self.env.user.write({
                    'phadata_user_name': company_data['name'],
                    'phadata_dtid': company_data['dtid'],
                    'phadata_user_idNo': company_data['identity']
                })
    
    @api.model
    def get_users(self):
        user_id = self.env.user.id
        rs = self.search([('create_uid', '=', user_id)])
        users = []
        for record in rs:
            dtid = record.phadata_dtid
            user_name = record.phadata_user_name
            if not dtid:
                dtid = '-'
            if not user_name:
                user_name = '-'
            user = {
                "account": record.login,
                "dtid": dtid,
                "username": user_name,
                "phone": self.env.company.phone,
                "role": False
            }
            users.append(user)
        return users
