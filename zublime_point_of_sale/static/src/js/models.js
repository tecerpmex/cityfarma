odoo.define('zublime_pos_extra_fee.models', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    const utils = require('web.utils');
    const field_utils = require('web.field_utils');
    const round_pr = utils.round_precision;

    models.load_fields('pos.payment.method', ['extra_fee']);

    const _super_paymentline = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
        get_extra_fee: function () {
            return this.amount * this.payment_method.extra_fee / 100;
        },
        get_extra_fee_str: function () {
            return field_utils.format.float(this.payment_method.extra_fee, {digits: [69, this.pos.currency.decimals]});
        },
        get_amount_with_extra_fee: function () {
            return round_pr(this.amount + this.get_extra_fee(), this.pos.currency.rounding);
        },      
    });

    const _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function() {
            const self = this;
            const receipt = _super_order.export_for_printing.apply(this, arguments);
            receipt.total_extra_fee = self.get_total_extra_fee();
            return receipt;
        },
        get_total_extra_fee: function() {
            return round_pr(this.paymentlines.reduce((function(sum, paymentLine) {
                sum += paymentLine.get_extra_fee();
                return sum;
            }), 0), this.pos.currency.rounding);
        },
    });

});
