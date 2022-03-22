import json

from odoo import http
from odoo.http import request
import requests
import logging

BASE_URL = 'https://ca.tdaas.dev.phadata.net'
# 贵州CA的通知地址
notifyUrl = "https://ca.tdaas.dev.phadata.net/api/v1/cert/apply/receive"


class CertController(http.Controller):

    @http.route('/count', type='http', auth='none')
    def count(self, **kwargs):
        result = requests.get('https://www.baidu.com')
        return result.content

    @http.route('/api/v1/apply-cert', type='json', auth='none')
    def applyCert(self, identNo, enterpriseName, callBackUrl):
        """
        申请证书的接口
        参数
            identNo:企业统一信用码不能为空
            enterpriseName:企业名称不能为空
            notifyUrl:后端通知回调URL不能为空
            callBackUrl:前端返回URL不能为空
        返回
            TODO
        """
        applyCertUrl = BASE_URL + '/api/v1/cert/applyCert'
        reqData = {
            "identNo": identNo,
            "enterpriseName": enterpriseName,
            "notifyUrl": notifyUrl,
            "callBackUrl": callBackUrl
        }
        # print(reqData)
        result = requests.post(applyCertUrl, None, reqData)
        # print(result.content)
        return json.loads(result.content)

    @http.route('/api/v1/find-and-save-cert', type='json', auth='user')
    def findAndSaveCert(self, resultId):
        """
        通过resultId查询并保存证书
        """
        # 判断此resultId对应的证书已存在就不做操作
        cert_query = request.env['tj.cert'].sudo().search([('result_id', '=', resultId)])
        read_data = cert_query.read()
        if read_data:
            read_data0 = read_data[0]
            payload = {
                "identNo": read_data0['ident_no'],
                "serialnumber": read_data0['serialnumber'],
                "signCert": read_data0['sign_cert'],
                "uniqueCode": read_data0['unique_code']
            }
            return {
                "code": "200000",
                "message": "证书已存在",
                "payload": payload
            }
        sealFind = BASE_URL + '/api/v1/cert/getApplyResult'
        result = requests.get(sealFind + '?resultId=' + resultId)
        # print(result.content)
        certJson = json.loads(result.content)
        if certJson['code'] == '500000':
            return certJson
        # print(certJson['code'])
        # print(certJson['message'])
        # print(certJson['payload'])
        saveObj = certJson['payload']
        cert = {
            'ident_no': saveObj['identNo'],
            'serialnumber': saveObj['serialnumber'],
            'sign_cert': saveObj['signCert'],
            'unique_code': saveObj['uniqueCode'],
            'seal_id': None,
            'status': 0,
            'reason': None,
            'apply_date': None,
            'result_id': resultId,
            'create_uid': http.request.env.user.id,
            'write_uid': http.request.env.user.id
        }
        request.env['tj.cert'].sudo().create(cert)
        return json.loads(result.content)

    @http.route('/api/v1/push-seal-model', type='json', auth='none')
    def pushSealModel(self, serialnumber, sealId, remark):
        """
        TODO 待测试
        印模推送绑定的接口
        参数
                    certB64:证书的base64
                    imgB64:印模图片的base64
                    remark:备注信息
        返回
                    TODO
        """
        certInfo = request.env['tj.cert'].sudo().search([('serialnumber', '=', serialnumber)])
        sealInfo = request.env['tj.seal.manage'].sudo().search([('id', '=', sealId)])
        # print(certInfo.sign_cert)
        # print(sealInfo.seal_model_url)
        # imgB64 = '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'
        imgB64 = sealInfo.seal_model_url
        pushSealModel = BASE_URL + '/api/v1/seal/pushSealModel'

        sealModelBindCertDTO = {
            "certB64": certInfo.sign_cert,
            "imgB64": imgB64,
            "remark": remark
        }
        result = requests.post(pushSealModel, None, sealModelBindCertDTO)
        data = json.loads(result.content)
        if data:
            # 添加证书和印章图片的绑定关系
            cert_sql_update = """ UPDATE tj_cert set status={},seal_id={} WHERE serialnumber='{}' """.format(0, sealId,
                                                                                                             serialnumber)
            print(cert_sql_update)
            request.cr.execute(cert_sql_update)
            # 去更新印模中的状态为待审核
            seal_sql_update = """ UPDATE tj_seal_manage set status=1,serialnumber='{}' WHERE id={} """.format(
                serialnumber, sealId)
            print(seal_sql_update)
            request.cr.execute(seal_sql_update)
        # print(result.content)
        return json.loads(result.content)

    @http.route('/api/v1/find-seal-status', type='json', auth='none')
    def findSealStatus(self, id):
        """
        TODO 待测试
        查询待审核的印章是否审核结束【其实就是主动同步贵州CA的审核状态】
        """
        querySealMode = '/api/v1/seal/querySealMode'

        if id:
            seal = request.env['tj.seal.manage'].sudo().search([('id', '=', id)])
            if seal:
                result = requests.post(BASE_URL + querySealMode, None, {
                    "trustNo": "",
                    "userId": "",
                    "certId": seal.serialnumber
                })
                if result:
                    data = json.loads(result.content)
                    if "200000" == data['code']:
                        payload = data['payload']
                        if payload:
                            status = payload[0]['status']
                            reason = payload[0]['reason']
                            # 证书的编号serialnumber
                            certId = payload[0]['certId']
                            logging.info("查询印章审核结果 证书序列号 %s,状态 %s,审核原因 %s" % (certId, status, reason))
                            # 状态 -1:禁用 -2：已删除 0：待审核 1：正常 2：审核不通过
                            if status == '1':
                                # 1 将cert表中的状态改为审核通过
                                # 证书绑定印模后，ca审核的状态[0: 待审核  1:审核通过  2:审核不通过]
                                logging.info("更新印章状态将cert表证书：%s;状态更新为：%s;原因更新为:%s" % (certId, 1, reason))
                                cert_sql = """ UPDATE tj_cert set status={},reason='{}' WHERE serialnumber='{}'""".format(
                                    1, reason, certId)
                                request.cr.execute(cert_sql)
                                # //2. 将seal表中的状态改为审核通过
                                # //印模的可用状态（0: 不可用 1:待审核  2:审核通过  3:审核不通过）
                                seal_sql = """ UPDATE tj_seal_manage set status={},reason='{}' WHERE serialnumber='{}'""".format(
                                    2, reason, certId)
                                logging.info("更新印章状态将seal表证书：%s;状态更新为：%s;原因更新为:%s" % (certId, 2, reason))
                                request.cr.execute(seal_sql)
                                print("更新sql %s \n %s" % (cert_sql, seal_sql))
                                return {
                                    "code": "200000",
                                    "message": "success",
                                    "payload": None
                                }
                            elif status == '0':
                                # 审核不通过
                                # //1 将cert表中的状态改为审核通过
                                # //证书绑定印模后，ca审核的状态[0: 待审核  1:审核通过  2:审核不通过]
                                cert_sql = """ UPDATE tj_cert set status={},reason='{}' WHERE serialnumber='{}'""".format(
                                    0, reason, certId)
                                logging.info("更新印章状态将cert表证书：%s;状态更新为：%s;原因更新为:%s" % (certId, 0, reason))
                                request.cr.execute(cert_sql)
                                # //2. 将seal表中的状态改为审核通过
                                # //印模的可用状态（0: 不可用 1:待审核  2:审核通过  3:审核不通过）
                                seal_sql = """ UPDATE tj_seal_manage set status={},reason='{}' WHERE serialnumber='{}'""".format(
                                    1, reason, certId)
                                logging.info("更新印章状态将seal表证书：%s;状态更新为：%s;原因更新为:%s" % (certId, 1, reason))
                                request.cr.execute(seal_sql)
                                print("更新sql %s \n %s" % (cert_sql, seal_sql))
                                return {
                                    "code": "200000",
                                    "message": "success",
                                    "payload": None
                                }
                            else:
                                logging.info("更新印章状态将cert表证书：%s;状态更新为：%s;原因更新为:%s" % (certId, 2, reason))
                                cert_sql = """ UPDATE tj_cert set status={},reason='{}' WHERE serialnumber='{}'""".format(
                                    2, reason, certId)
                                request.cr.execute(cert_sql)
                                seal_sql = """ UPDATE tj_seal_manage set status={},reason='{}' WHERE serialnumber='{}'""".format(
                                    3, reason, certId)
                                logging.info("更新印章状态将seal表证书：%s;状态更新为：%s;原因更新为:%s" % (certId, 3, reason))
                                request.cr.execute(seal_sql)
                                print("更新sql %s \n %s" % (cert_sql, seal_sql))
                    return {
                        "code": "200000",
                        "message": "success",
                        "payload": {
                            "message": data['message'],
                        }
                    }

    @http.route('/test', type='http', auth='none', methods=['GET'], cors='*')
    def test(self):
        print('resultId')
        return 'resultId'

    @http.route('/api/v1/seal-list', type='json', auth='user')
    def sealList(self, status):
        """
        查询印章列表
        status: 印模的可用状态（0: 不可用 1:待审核  2:审核通过  3:审核不通过）
        """
        if status is None or status == -1:
            result = request.env['tj.seal.manage'].sudo().search([])
        else:
            result = request.env['tj.seal.manage'].sudo().search([('status', '=', status)])
        print(request.env.is_admin())
        if request.env.is_admin():
            # 返回所有
            print(result.read())
            all = {
                "code": "200000",
                "message": "success",
                "payload": result.read()
            }
            return all
        # 查询当前用户的印章授权列表
        print(request.env.user.id)
        current_user_id = request.env.user.id
        # current_user_id = 2
        sealAuth = request.env['tj.seal.auth'].sudo().search([('user_id', '=', current_user_id)])
        sa_ids = sealAuth.ids
        if len(sa_ids) <= 0:
            return {
                "code": "200000",
                "message": "当前用户没有印章",
                "payload": []
            }
        sa_data = sealAuth.read()
        resultData = []
        result_read = result.read()
        for item in result_read:
            for sa in sa_data:
                # 判断当前将当前用户拥有授权的印章数据返回
                if item['id'] == sa['seal_id']:
                    # print(item)
                    resultData.append(item)
        return {
            "code": "200000",
            "message": "success",
            "payload": resultData
        }

    @http.route('/api/v1/company-info', type='json', auth='user')
    def companyInfo(self):
        """
        查询但前企业的信息
        """
        print('查询dtid和当前企业名称')
        company_name = request.env.company.name
        phadata_company_code = request.env.company.phadata_company_code
        dtid = request.env.user.phadata_dtid
        data = {
            "companyName": company_name,
            "dtid": dtid,
            "identNo": phadata_company_code
        }
        # print("companyInfo:", data)
        return {
            "code": "200000",
            "message": "查询成功",
            "payload": data
        }
