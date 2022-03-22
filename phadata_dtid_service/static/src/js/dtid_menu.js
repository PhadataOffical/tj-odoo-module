odoo.define('web.dtidMenu', function (require) {
    "use strict";
    
    const core = require('web.core');
    const UserMenu = require('web.UserMenu');
    const Dialog = require('web.Dialog');
    const _t = core._t;
    const QWeb = core.qweb;
    
    UserMenu.prototype._onMenuDtid = function () {
        const self = this;
        const session = self.getSession();

        // call model
        self._rpc({
            model: 'res.users', 
            method: 'get_dtid'
        }).then(function(data) {
            console.log(data)
            if (!data.dtid) {
                // call controller
                self._rpc({route: '/get/qrcode'})
                    .then(function (data) {
                        const dialog = new Dialog(this, {
                            size: 'large',
                            dialogClass: 'o_act_window',
                            title: _t("DTID"),
                            $content: $(QWeb.render('DtidMenu.Auth', {
                                "qrcode_content": data,
                                "is_admin": session.is_admin
                            })),
                        })
                        dialog.open()
                        let timer = setInterval(get_scan_core_result, 1000 * 5);
                        function get_scan_core_result() {
                            self._rpc({route: '/get/scan', params: {'qrId': data.qrId}})
                                .then(data => {
                                    if (data.code == '200000') {
                                        self._rpc({
                                            model: 'res.users',
                                            method: 'update_dtid',
                                            kwargs: {
                                                "company_data": data.payload,
                                                "is_admin": session.is_admin
                                            }
                                        }).then(res => {
                                            window.location.reload();
                                        })
                                        clearInterval(timer)
                                    } else {
                                        console.log(data.message)
                                    }
                                })
                        }

                })
            } else {
                self._rpc({
                    model: 'res.users',
                    method: 'get_users'
                }).then(res => {
                    const dialog = new Dialog(this, {
                        size: 'large',
                        dialogClass: 'o_act_window',
                        title: _t("DTID"),
                        $content: $(QWeb.render('DtidMenu.Info', {
                            'data': data,
                            'role': session.is_admin,
                            'users': res,
                        })),
                    });
                    dialog.opened().then(function () {
                        $('.show-license').click(function() {
                            new Dialog(this, {
                                size: 'large',
                                dialogClass: 'o_act_window',
                                title: _t("Business License"),
                                $content: $(QWeb.render('DtidMenu.License', {
                                    'license': data.license_b64,
                                }))
                            }).open();
                        });
                    });
                    dialog.open();
                    // const params = {
                    //     'pdf_base64': data.license_b64
                    // }

                    // self.do_action({
                    //     'type': 'ir.actions.client',
                    //     'name': 'PDF',
                    //     'tag': 'dtid.license.pdf.page',
                    //     'target': 'new',
                    //     'params': params,
                    //     'context': params
                    // });
                })
            }
        })
    }
    
    return UserMenu;
    
});
    