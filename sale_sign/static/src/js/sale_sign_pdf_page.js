odoo.define('Sale.SignPdfPage', function(require) {
    const core = require('web.core')
    const action = require('web.AbstractAction')

    const page = action.extend({
        template: 'SaleSignPdfPage',

        init: function(parent, action) {
            this._super(parent, action);
            this.params = {
                sign_id: action.params.sign_id,
                order_id: action.params.order_id,
                pdf_url: action.params.pdf_url,
                pdf_base64: action.params.pdf_base64,
            };
        },

        async start() {
            this.$el.html(
                core.qweb.render('SaleSignPadEmbed', {
                    pdfurl: this.params.pdf_url,
                })
            )
        },

    });

    core.action_registry.add('sale.sign.pdf.page', page)

    return page;
})