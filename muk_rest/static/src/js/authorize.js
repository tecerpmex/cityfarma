odoo.define('muk_rest.authorize', function (require) {
'use strict';

require('web.dom_ready');

var ajax = require('web.ajax');
var core = require('web.core');

var _t = core._t;

if(!$('.mk_authorize').length) {
    return $.Deferred().reject("DOM doesn't contain '.mk_authorize'");
}

$('[data-toggle="popover"]').popover({
	html: true,
	content: function() {
		var $popover = $(this);
		var reference = $(this).data('content-id');
	    if($popover.find(reference).length) {
	    	return $popover.find(reference).html();
	    }
	}
})

});
