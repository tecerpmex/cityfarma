odoo.define('zublime_pos_extra_fee.models', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    const utils = require('web.utils');
    const round_pr = utils.round_precision;

    models.load_fields('pos.payment.method', ['extra_fee']);

    const _super_paymentline = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
        get_extra_fee: function () {
            return this.amount * this.payment_method.extra_fee / 100;
        },
        get_amount: function() {
            return this.amount + this.get_extra_fee();
        },
        get_amount_str: function(){
            return field_utils.format.float(this.get_amount(), {digits: [69, this.pos.currency.decimals]});
        },
        
    });

    const _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_as_JSON: function() {
            const self = this;
            const json = _super_order.export_as_JSON.apply(this, arguments);
            const extra_fee = self.get_total_extra_fee();
            json.total_extra_fee = extra_fee;
            json.amount_total += extra_fee;
            return json;
        },
        export_for_printing: function() {
            const self = this;
            const receipt = _super_order.export_for_printing.apply(this, arguments);
            const extra_fee = self.get_total_extra_fee();
            receipt.total_extra_fee = extra_fee;
            receipt.total_with_tax += extra_fee;
            receipt.total_rounded += extra_fee;
            return receipt;
        },
        get_total_extra_fee: function() {
            return round_pr(this.paymentlines.reduce((function(sum, paymentLine) {
                sum += paymentLine.get_extra_fee();
                return sum;
            }), 0), this.pos.currency.rounding);
        },
        get_change: function(paymentline) {
            if (!paymentline) {
                var change = this.get_total_paid() - this.get_total_with_tax() - this.get_total_extra_fee() - this.get_rounding_applied();
            } else {
                var change = -this.get_total_with_tax();
                var lines  = this.paymentlines.models;
                for (var i = 0; i < lines.length; i++) {
                    change += lines[i].get_amount();
                    if (lines[i] === paymentline) {
                        break;
                    }
                }
            }
            return round_pr(Math.max(0, change), this.pos.currency.rounding);
        },    
        get_due: function(paymentline) {
            if (!paymentline) {
                var due = this.get_total_with_tax() + this.get_total_extra_fee() - this.get_total_paid() + this.get_rounding_applied();
            } else {
                var due = this.get_total_with_tax();
                var lines = this.paymentlines.models;
                for (var i = 0; i < lines.length; i++) {
                    if (lines[i] === paymentline) {
                        break;
                    } else {
                        due -= lines[i].get_amount();
                    }
                }
            }
            return round_pr(due, this.pos.currency.rounding);
        },
    });

});
