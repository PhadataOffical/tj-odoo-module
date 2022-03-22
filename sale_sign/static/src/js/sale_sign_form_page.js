odoo.define('Sale.SignFormPage', function(require) {
    const core = require('web.core')
    const action = require('web.AbstractAction')
    var QWeb = core.qweb

    //固定的印章大小和pdf大小
    const sealSize = 127.5
    const PdfSize = 595
    const PdfSizeHeight = 813.7

    let sealPostion = {
        left: 416.5,
        top: 488.22,
    }

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

    const page = action.extend({
        template: 'SaleSignFormPage',
        events: {
            'click .tj-contract-sign-seal': '_onChooseSeal',
            'click .dosign-btn': '_onSign',
            'change .tj-seal-pos-control': '_onPosChange',
            'change .tj-back-btn': 'goSealListPage',
        },

        init: function(parent, action) {
            this._super(parent, action)
            this.params = {
                isrefresh: !action.params.seals, //false即为刷新页面
                seals: action.params.seals,
                order_id: action.params.order_id,
                html_url: window.location.origin + action.params.html_url,
                pdf_url: window.location.origin + action.params.pdf_url,
            }
            // this._rpc({route: '/tj/sale-sign/order/sign', params: {
            //         order_id: this.params.order_id, x: 0, y: 0, w:100, h: 100,
            //         seal_id: (this.params.seals.length > 0)?this.params.seals[0].id:0,
            //         callBackUrl: ''
            // }}).then(data=>{
            //     console.log('init.sign.rpc', data);
            // }).catch(e=>{
            //     console.log('init.sign.catch', e);
            // });
            // const orderId = '21';  //  this.params.order_id
            // const result_id = '622affa3e6947c42e58351f8';
            // this._rpc({route: '/tj/sale-sign/order/sign/result', params: {
            //         result_id: result_id,
            //         order_id: orderId
            //     }}).then(data=>{
            //     console.log('init.result.rpc', data);
            // }).catch(e=>{
            //     console.log('init.result.catch', e);
            // });
        },

        async start() {
            this.selectedSeal = null
                // tj.ca.sign.callback.page
            if (!this.params.seals) {
                let seals = await this.getSeals()
                if (seals) this.params.seals = seals
            }
            this.initPage()
        },

        initPage() {
            let params = getParams()
            if (params.resultId) {
                this.$el.html(
                    QWeb.render('tj.ca.sign.callback.page', {
                        isloading: true,
                    })
                )

                this.updateSignState(params.resultId, params.orderId)
                return
            } else if (params.back && this.params.isrefresh) {
                setTimeout(function() {
                    $('.o_menu_brand')[0].click()
                }, 1000)
                return
            }
            this.$el.html(
                QWeb.render('ContractSign.page', {
                    pdfurl: this.params.pdf_url,
                    htmlurl: this.params.html_url,
                    seals: this.params.seals,
                    getSealUrl: this._getSealUrl.bind(this),
                })
            )
        },

        updateSignState(result_id, orderId) {
            const self = this
            this._rpc({
                    route: '/tj/sale-sign/order/sign/result',
                    params: {
                        result_id: result_id,
                        order_id: orderId,
                    },
                })
                .then(function(res) {
                    if (res.code === '200000') {
                        self.$el.html(
                            QWeb.render('tj.ca.sign.callback.page', {
                                isloading: false,
                            })
                        )
                        setTimeout(function() {
                            self.goSealListPage()
                        }, 5000)
                    }
                })
                .catch((e) => {
                    console.log('报错了吗？', e)
                })
        },
        getPictureList() {
            try {
                let datas = [{
                    downloadUrl: 'https://contract.tdaas.test.phadata.net/api/v1/file/download/1500652932062773248',
                    fileId: '1500652932062773248',
                    fileName: null,
                    id: '1782',
                    order: 1,
                    previewUrl: 'https://contract.tdaas.test.phadata.net/api/v1/file/preview/1500652932062773248',
                    templateParams: null,
                }, ]

                return datas
            } catch (error) {}
        },

        async getSeals() {
            let res = await this._rpc({ route: '/api/v1/seal-list', params: { status: 2 } })

            if (res.code === '200000' && res.payload) {
                return res.payload
            }
            return []
        },

        _getSealUrl: function(base64) {
            return URL.createObjectURL(dataURItoBlob(base64))
            return 'https://tj3agep56jqhhhej4frkejnmwmf3nk.tdaas.test.phadata.net/serverurl' + url
        },

        _onChooseSeal(e) {
            let dataset = e.currentTarget.dataset
            let selectedSeal = {
                id: dataset.id,
                serialnumber: dataset.serialnumber,
                seal_model_url: dataset.sealmodelurl,
            }
            this.selectedSeal = selectedSeal
            $('.tj-sign-seals-contrainer').html(
                QWeb.render('ContractSign.seal', {
                    getSealUrl: this._getSealUrl.bind(this),
                    selectedSeal: selectedSeal,
                })
            )
            $('.tj-contract-sign-seal-selected').css({ left: sealPostion.left + 'px', top: sealPostion.top + 'px' })
        },

        //设置位置修改
        _onPosChange(e) {
            var value = e.target.value
            var type = e.currentTarget.dataset.type
            value = Number(value)
            if (type === 'top') {
                sealPostion[type] = PdfSizeHeight * (value / 100)
            } else {
                sealPostion[type] = PdfSize * (value / 100)
            }

            $('.tj-contract-sign-seal-selected').css({ left: sealPostion.left + 'px', top: sealPostion.top + 'px' })
        },

        // 确认签署合约
        _onSign: function(e) {
            e.stopPropagation()
            e.preventDefault()

            // const top = (PdfSizeHeight * sealPostion.top) / 100
            // const left = (PdfSize * sealPostion.left) / 100

            if (!this.selectedSeal) {
                alert("您还没有选择印章！")
                return;
            }
            const top = sealPostion.top
            const left = sealPostion.left

            const callBackUrl = window.location.origin + window.location.pathname + '?sealId=' + this.selectedSeal.id + '&orderId=' + this.params.order_id + window.location.hash

            this._rpc({
                    route: '/tj/sale-sign/order/sign',
                    params: {
                        order_id: this.params.order_id,
                        x: left,
                        y: top,
                        w: sealSize,
                        h: sealSize,
                        seal_id: this.selectedSeal.id,
                        callBackUrl: callBackUrl,
                    },
                })
                .then((res) => {
                    if (res.code === '200000') {
                        window.location.href = res.payload.data
                    }
                })
                .catch((e) => {
                    console.log('init.sign.catch', e)
                })
        },
        //跳回印章列表页面
        goSealListPage() {
            const callBackUrl = window.location.origin + window.location.pathname + '?back=1' + window.location.hash
            window.location.href = callBackUrl
            setTimeout(() => {
                $('.o_menu_brand')[0].click()
            }, 1000)
            return
        },
    })

    core.action_registry.add('sale.sign.form.page', page)

    return page
})
