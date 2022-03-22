import json

from odoo import http
from odoo.http import request
import psycopg2 as pg2


def get_db_conn():
    # 创建连接
    return pg2.connect(database='odoo14', user='odoo', password='123456', host='192.168.1.100', port='5432')


class SealController(http.Controller):

    @http.route('/seal/add', type='json', auth='none')
    def AddSeal(self, **vals):
        # print(vals)
        vals['create_uid'] = request.env.user.id
        # print(vals)
        result = request.env['tj.seal.manage'].sudo().create(vals)
        # print(result)
        return {
            "code": "200000",
            "message": "success",
            "payload": None
        }

    @http.route('/seal/update', type='json', auth='none')
    def UpdateSeal(self, **vals):
        # print(vals)
        vals['create_uid'] = request.env.user.id
        # print(vals)
        seal = request.env['tj.seal.manage'].sudo().search([('id', '=', vals['id'])])
        # print(seal)
        seal.write(vals)
        return {
            "code": "200000",
            "message": "success",
            "payload": None
        }

    @http.route('/seal/delete', type='json', auth='none')
    def DeleteSeal(self, id):
        seal = request.env['tj.seal.manage'].sudo().search([('id', '=', id)])
        # print(seal)
        seal.unlink()
        return {
            "code": "200000",
            "message": "success",
            "payload": None
        }

    @http.route('/seal/add-auth-seal', type='json', auth='none')
    def AddAuth(self, sealId, userId):
        res = request.env['tj.seal.manage'].sudo().search([('id', '=', sealId)])
        """
         判断 seal是否存在
        """
        if res.status != 2:
            print("印章未审核")
            return {
                "code": "400000",
                "message": "印章未审核",
                "payload": None
            }

        sql = """
        SELECT * FROM tj_seal_auth WHERE seal_id={} and user_id={}
        """.format(sealId, userId)
        request.env.cr.execute(sql)
        seal_auth = request.cr.fetchall() or []

        print(seal_auth)
        if seal_auth:
            print("已授权")
            return {
                "code": "400000",
                "message": "已授权",
                "payload": None
            }

        seal_auth_val = {
            "seal_id": sealId,
            "user_id": userId,
        }
        seal_auth_save = request.env['tj.seal.auth'].sudo().create(seal_auth_val)
        print(seal_auth_save)
        print('添加授权完成')
        return {
            "code": "200000",
            "message": "success",
            "payload": None
        }

    @http.route('/seal/delete-auth-seal', type='json', auth='none')
    def DeleteAuth(self, sealId, userId):
        """
         TODO 删除带实现
        """
        sql = """
        DELETE  FROM tj_seal_auth WHERE seal_id={} and user_id={}
        """.format(sealId, userId)
        print(sql)
        request.cr.execute(sql)
        # conn = get_db_conn()
        # cur = conn.cursor()
        # cur.execute(sql)
        #
        # conn.commit()
        # cur.close()
        # conn.close()

        print(sealId)
        print(userId)

        return {
            "code": "200000",
            "message": "success",
            "payload": None
        }

    @http.route('/seal/find-seals-auth', type='json', auth='none')
    def FindAuthsById(self, sealId):
        """
         查看某个印章的授权用户列表
         TODO
        """
        print(sealId)
        seal = request.env['tj.seal.manage'].sudo().search([('id', '=', sealId)])
        if not seal:
            return {
                "code": "400000",
                "message": "印章不正确",
                "payload": None
            }

        sql = """
            SELECT * FROM res_users WHERE id 
             IN 
            (SELECT user_id FROM tj_seal_auth WHERE seal_id ={} ) AND res_users.active=TRUE
            """.format(sealId)

        request.cr.execute(sql)
        seal_users = request.cr.fetchall() or []
        payload = []
        for rs in seal_users:
            user = {
                "id": rs[0],
                "account": rs[2],
                "dtid": rs[18],
                "name": rs[19],
            }
            payload.append(user)
        return {
            "code": "200000",
            "message": "success",
            "payload": payload
        }

    @http.route('/seal/find-seals-not-auth', type='json', auth='none')
    def FindNotAuthsById(self, sealId):
        """
         查看某个印章未授权用户列表
         TODO
        """
        print(sealId)
        seal = request.env['tj.seal.manage'].sudo().search([('id', '=', sealId)])
        if not seal:
            return {
                "code": "400000",
                "message": "印章不正确",
                "payload": None
            }
        sql = """
            SELECT * FROM res_users WHERE id 
            NOT IN 
            (SELECT user_id FROM tj_seal_auth WHERE seal_id ={}) AND res_users.active=TRUE
            """.format(sealId)

        # print(sql)
        request.cr.execute(sql)
        seal_users = request.cr.fetchall() or []
        # print(seal_users)
        payload = []
        for rs in seal_users:
            user = {
                "id": rs[0],
                "account": rs[2],
                "dtid": rs[18],
                "name": rs[19],
            }
            payload.append(user)
        return {
            "code": "200000",
            "message": "success",
            "payload": payload
        }
