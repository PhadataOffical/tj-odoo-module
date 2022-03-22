# -*- coding: utf-8 -*-
import json

import requests

from ..controllers import api
from ..util import aes

DTID_SERVER = "https://dtid.tdaas.dev.phadata.net"
DTID_REGISTER_URI = DTID_SERVER + "/api/v1/dtid/registry/create"
DTID_BIND_SERVER = "https://bind.tdaas.dev.phadata.net"
DTID_BIND_DTID_URI = DTID_BIND_SERVER + "/api/v1/bind/document"


def registry_dtid():
    resp = requests.post(url=DTID_REGISTER_URI, json={"safeCode": ""})
    if resp.status_code == api.HTTP_OK:
        api_result = api.parser(resp.json())
        if api_result.code == api.SUCCESS:
            return api_result.payload


def bind_company_dtid(dtid_document, company_data):
    auth_info = {
        "type": "SAMR",
        "unionId": company_data['licencesn'],
        "state": 1,
        "desc": "已进行企业认证服务",
        "name": company_data['entname'],
        "idNo": company_data['uniscid']
    }
    params = {
        "document": dtid_document,
        "authInfo": auth_info,
        "targetId": "auth",
        "tdrType": "10002"
    }

    raw = json.dumps(params).encode()
    bizSign = aes.AESCipher().encrypt(raw)
    requestData = {
        "bizSign": bizSign
    }
    resp = requests.post(url=DTID_BIND_DTID_URI, json=requestData)
    if resp.status_code == api.HTTP_OK:
        result = api.parser(resp.json())
        if result.code == api.SUCCESS:
            return result.payload

