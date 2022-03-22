
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { _lt } from "@web/core/l10n/translation";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks";


class IdentityDialog extends Dialog {
    setup() {
        super.setup();
        this.data = this.props.data;
        this.dialog = useService("dialog")
    }
    showLicense() {
        this.dialog.add(LicenseDialog, {
            data: {
                "license_b64": this.data.dtidData.license_b64,
            }
        });
    }
}
IdentityDialog.title = _lt("Identity");

class AuthDialog extends Dialog {
    setup() {
        super.setup();
        this.data = this.props.data
    }
}
AuthDialog.title = _lt("Identity Auth")

class LicenseDialog extends Dialog {
    setup() {
        super.setup();
        this.data = this.props.data;
    }
}
LicenseDialog.title = _lt("Business License")
LicenseDialog.bodyTemplate = "DtidMenu.License";

function IdentityItem(env) {
    
    return {
        type: "item",
        id: "identity",
        description: env._t("Identity"),
        callback: async () => {
            const dtidData = await env.services.orm.call("res.users", "get_dtid");
            const dtid = dtidData.dtid
            if (!dtid) {
                AuthDialog.bodyTemplate = "DtidMenu.Auth";
                await env.services
                    .rpc("/get/qrcode")
                    .then((data) => {
                        env.services.dialog.add(AuthDialog, {
                            data: {
                                "content": data,
                                "isAdmin": session.is_admin
                            }
                        });
                        const timer = setInterval(() => {
                            env.services.rpc("/get/scan", {
                                'qrId': data.qrId
                            }).then((data) => {
                                if (data.code == "200000") {
                                    const updateResult = env.services.orm
                                        .call("res.users", "update_dtid", [], {
                                            company_data: data.payload,
                                            is_admin: session.is_admin,
                                    });
                                    updateResult.then( () => {
                                        window.location.reload();
                                    }).catch(() => {
                                        console.log("error")
                                    });
                                    clearInterval(timer)
                                } else {
                                    console.log(data.message)
                                }

                            })
                            .catch(() => {
                                console.log("error")
                            });
                        }, 1000 * 5);

                    })
                    .catch(() => {
                        console.log("error")
                    });
            } else {
                const userData = await env.services.orm.call("res.users", "get_users");
                IdentityDialog.bodyTemplate = "DtidMenu.Info";
                env.services.dialog.add(IdentityDialog, {
                    data: {
                        "dtidData": dtidData,
                        "role": session.is_admin,
                        "userData": userData,
                    }
                });
            }
            
        },
        sequence: 45,
    };
}


registry.category("user_menuitems").add('identity', IdentityItem, { force: true })

