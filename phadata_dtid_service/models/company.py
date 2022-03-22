# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..controllers import company as companyApi


class PhadataCompanyModel(models.Model):
    _inherit = 'res.company'
    _description = 'phadata_company_model'

    phadata_company_auth_status = fields.Integer()
    phadata_company_code = fields.Char()
    phadata_company_frname = fields.Char()
    phadata_company_name = fields.Char()
    phadata_company_dtid = fields.Char()
    phadata_company_license_b64 = fields.Text()

    @api.model
    def update_company(self, company_data, dtid):
        
        imageurl = company_data["imageurl"]
        print(imageurl)
        if imageurl:
            phadata_company_license_b64 = companyApi.get_license_b64(imageurl)
        self.env.company.write({
            "phadata_company_auth_status": 1,
            "phadata_company_code": company_data["uniscid"],
            "phadata_company_frname": company_data["name"],
            "phadata_company_name": company_data["entname"],
            "phadata_company_dtid": dtid,
            "name": company_data["entname"],
            "company_registry": company_data["uniscid"],
            "phadata_company_license_b64": phadata_company_license_b64
        })
