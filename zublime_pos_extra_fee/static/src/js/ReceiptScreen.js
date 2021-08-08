odoo.define('zublime_pos_extra_fee.ReceiptScreen', function(require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const PosExtraFeeReceiptScreen = ReceiptScreen =>
        class extends ReceiptScreen {
            get orderAmountPlusTip() {
                const order = this.currentOrder;
                const orderTotalAmount = order.get_total_with_tax() + order.get_total_extra_fee();
                const tip_product_id = this.env.pos.config.tip_product_id && this.env.pos.config.tip_product_id[0];
                const tipLine = order
                    .get_orderlines()
                    .find((line) => tip_product_id && line.product.id === tip_product_id);
                const tipAmount = tipLine ? tipLine.get_all_prices().priceWithTax : 0;
                const orderAmountStr = this.env.pos.format_currency(orderTotalAmount - tipAmount);
                if (!tipAmount) return orderAmountStr;
                const tipAmountStr = this.env.pos.format_currency(tipAmount);
                return `${orderAmountStr} + ${tipAmountStr} tip`;
            }
        };

    Registries.Component.extend(ReceiptScreen, PosExtraFeeReceiptScreen);

    return ReceiptScreen;
});