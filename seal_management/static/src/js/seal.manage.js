function getParams() {
    let params = {}
        // let search = window.location.search
        //   search
    let strs = window.location.search.substring(1).split('&')
    if (strs.length > 0) {
        strs.map((str) => {
            let vals = str.split('=')
            params[vals[0]] = decodeURIComponent(vals[1])
            return str
        })
    }

    return params
}

odoo.define('tj.seal.manage', function(require) {
    var AbstractAciton = require('web.AbstractAction')
    var core = require('web.core')
    var QWeb = core.qweb
    const _t = core._t
    const Dialog = require('web.Dialog')

    function dataURItoBlob(base64Data) {
        if (!base64Data.startsWith('data:')) {
            base64Data = 'data:image/png;base64,' + base64Data
        }
        var byteString
        if (base64Data.split(',')[0].indexOf('base64') >= 0) byteString = atob(base64Data.split(',')[1])
            //base64 解码
        else {
            byteString = unescape(base64Data.split(',')[1])
        }
        var mimeString = base64Data.split(',')[0].split(':')[1].split(';')[0] //mime类型 -- image/png

        var ia = new Uint8Array(byteString.length) //创建视图
        for (var i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i)
        }
        var blob = new Blob([ia], {
            type: mimeString,
        })
        return blob
    }

    //绘制印章
    function drawSealImg(canvasid, sealName, typeName) {
        let seal = new Seal('#' + canvasid, {
            radius: 110, // 默认半径75px
            color: 'red', // 默认颜色红色
            companyName: sealName, // 默认 上海妙一生物科技有限公司
            fontFamily: 'Helvetica', // 默认宋体
            typeName: typeName, // 印章类型 默认为空
            typeNameSize: 9, // 类型属性字体大小
            hasInnerLine: false, // 内边框 默认false
            securityCode: '', // 防伪码 只能为13位 默认空
        })
        seal.typeNameFontSize = 11
        seal._drawCompanyName()
        let img = seal.saveSealImg()

        // const file = dataURLtoFile('png', img, sealName + '.png')
        // const blob = URL.createObjectURL(dataURItoBlob(img))

        return img
            // setSealImage(blob)
    }
    var WebPage = AbstractAciton.extend({
        template: 'seal.card.list',
        events: {
            'click .tj-seal-create': '_goCreateSeal',
            'click .tj-seal-auth': '_onSealAuthManager',
            'click .tj-seal-bingca': '_goBindCa',
            'click .tj-catoseallist-btn': 'goSealListPage',
        },
        start: async function() {
            const self = this
            this.companyInfo = null
            await this.getCompanyInfo()
            this.initSeallist()
        },
        init: function(parent, action) {
            this._super(parent, action)

            let session = this.getSession()
            this.is_admin = session.is_admin;
        },

        async initSeallist() {
            let params = getParams()
            const self = this;

            if (params.resultId) {
                this.$el.html(
                    QWeb.render('tj.ca.callback.page', {
                        isloading: true,
                    })
                )

                this.bindCaToSeal(params.resultId, params.sealId)
                return
            }
            let seals = await this.getSeals()

            console.log("企业数据：", this.companyInfo);

            this.$el.html(
                QWeb.render('tj.seal.card.item', {
                    seals: seals,
                    is_admin: self.is_admin ? 1 : 0,
                    isDtid: this.companyInfo.dtid !== false,
                    getSealUrl: this._getSealUrl.bind(this),
                })
            )

            // 查询待审核的印章的审核结果
            for (let seal of seals) {
                if (seal.status === 1) {
                    this.getSealAuthStatus(seal.id)
                }
            }
        },

        async getCompanyInfo() {
            let res = await this._rpc({ route: '/api/v1/company-info' })
            if (res.code === '200000' && res.payload) {
                this.companyInfo = res.payload
            } else {
                this.companyInfo = null
            }
        },

        /**
         * -1:查询所有 0: 不可用 1:待审核 2:审核通过 3:审核不通过
         */
        async getSeals() {
            let res = await this._rpc({ route: '/api/v1/seal-list', params: { status: -1 } })

            if (res.code === '200000' && res.payload) {
                return res.payload
            }
            return []
        },

        getSealAuthStatus(id) {
            this._rpc({ route: '/api/v1/find-seal-status', params: { id: id } })
        },

        _getSealUrl: function(base64) {
            return URL.createObjectURL(dataURItoBlob(base64))
        },

        _goCreateSeal: function() {
            const self = this
            let dialog = new Dialog(this, {
                size: 'large',
                dialogClass: 'tj-create-seal',
                title: _t('创建印章'),
                buttons: [{
                    text: _t('创建'),
                    classes: 'btn-primary o_adyen_confirm',
                    close: false,
                    disabled: false,
                    click: async function() {
                        let valueArr = $('#tj_create_seal_form').serializeArray()
                        let values = {}
                        $.each(valueArr, function() {
                            values[this.name] = this.value
                        })
                        if (values.tjAgreeUse !== 'on') {
                            alert('请同意协议！')
                            return
                        }

                        delete values.tjAgreeUse
                        let seal_model_url = drawSealImg('seal_canvas', values.seal_name, values.seal_type_name)

                        values.seal_model_url = seal_model_url.split('base64,')[1]
                        let res = await self._rpc({ route: '/seal/add', params: values })
                        if (res.code === '200000') {
                            alert('创建成功！')
                            self.initSeallist()
                            dialog.close()
                        }
                    },
                }, ],
                $content: $(
                    QWeb.render('tj.seal.create', {
                        companyName: self.companyInfo.companyName,
                        companyDtid: self.companyInfo.dtid,
                    })
                ),
            }).open()
        },

        async changeUserAuth(isadd, sealId, userId) {
            const url = isadd ? "/seal/add-auth-seal" : "/seal/delete-auth-seal";
            let res = await this._rpc({ route: url, params: { sealId: sealId, userId: userId } })
            if (res.code === "200000") {
                alert(isadd ? "添加成功！" : "取消成功")
            }
        },

        async getAuthUserList(isauth, sealid) {
            let url = isauth ? '/seal/find-seals-auth' : '/seal/find-seals-not-auth'

            let res = await this._rpc({ route: url, params: { sealId: sealid } })

            if (res.code === '200000' && res.payload) {
                return res.payload
            }
        },

        addAuthEventListener() {
            const self = this
            $('.btn-change-sealauth-tab').unbind()
            $('.tj-btn-changeauth').unbind()

            //切换tab
            $('.btn-change-sealauth-tab').click(function(e) {
                let dataset = e.target.dataset
                self.changeAuthList(dataset.type === 'isauth', dataset.sid)
            })

            //授权/取消授权
            $('.tj-btn-changeauth').click(function(e) {
                let dataset = e.target.dataset
                self.changeUserAuth(dataset.type === "add", dataset.sid, dataset.uid)
            })
        },

        //授权列表tab改变
        async changeAuthList(isauth, sealid) {
            let userlists = await this.getAuthUserList(isauth, sealid)
            if (userlists) {
                this.renderAuthPage(isauth, sealid, userlists)
            }
        },

        // 渲染授权管理页面
        renderAuthPage(isauthtab, sealid, userlists) {
            if (this.authdialog) {
                this.authdialog.$el.html("");
                this.authdialog.$el.html(
                    QWeb.render('tj.seal.auth.manager.page', {
                        sealid: sealid,
                        isauthtab: isauthtab,
                        userlists: userlists,
                    })
                )
                this.addAuthEventListener()
                return
            }
            const self = this
            let dialog = new Dialog(this, {
                size: 'large',
                dialogClass: 'tj-auth-seal-dialog',
                title: _t('授权管理'),
                buttons: [],
                $content: $(
                    QWeb.render('tj.seal.auth.manager.page', {
                        sealid: sealid,
                        isauthtab: isauthtab,
                        userlists: userlists,
                    })
                ),
            })
            this.authdialog = dialog

            dialog.opened().then(function() {
                self.addAuthEventListener()
            })
            dialog.on('closed', null, () => {
                this.authdialog = null
            })

            dialog.open()
        },

        //印章授权管理
        _onSealAuthManager: async function(e) {
            const self = this
            const isauthtab = true; //默认是已授权用户列表
            var sealid = e.currentTarget.dataset.sid
            let userlists = await this.getAuthUserList(isauthtab, sealid)
            if (userlists) {
                this.renderAuthPage(isauthtab, sealid, userlists)
            }
        },

        //去绑定CA
        _goBindCa: async function(e) {
            let sealId = e.target.dataset.sid
            const callBackUrl = window.location.origin + window.location.pathname + '?sealId=' + sealId + window.location.hash
                // const callBackUrl = "https://www.baidu.com#a=123"

            // let identNo  = this.companyInfo.identNo
            // let companyName  = this.companyInfo.companyName

            let identNo = '91522701MA6DJ2PJ3T'
            let companyName = '凌辉建设工程咨询有限公司贵州分公司'

            let res = await this._rpc({ route: '/api/v1/apply-cert', params: { identNo: identNo, enterpriseName: companyName, callBackUrl: callBackUrl } })
            if (res.code === '200000' && res.payload) {
                window.location.href = res.payload
            }
        },

        async bindCaToSeal(resultId, sealId) {
            const self = this
            let res = await this._rpc({ route: '/api/v1/find-and-save-cert', params: { resultId } })
            if (res.code === '200000' && res.payload) {
                let resu = await this._rpc({ route: '/api/v1/push-seal-model', params: { remark: '绑定证书', sealId: sealId, serialnumber: res.payload.serialnumber } })

                if (resu.code === '200000') {
                    this.$el.html(
                        QWeb.render('tj.ca.callback.page', {
                            isloading: false,
                            serialnumber: res.payload.serialnumber,
                        })
                    )

                    setTimeout(function() {
                        self.goSealListPage()
                    }, 6000)
                }
                return
            }
        },

        //跳回印章列表页面
        goSealListPage() {
            const callBackUrl = window.location.origin + window.location.pathname + window.location.hash
            window.location.href = callBackUrl
        },
    })

    core.action_registry.add('tj.seal.manage', WebPage)
})