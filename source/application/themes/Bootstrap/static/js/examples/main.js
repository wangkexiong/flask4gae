var Utils = {
    renderFieldErrorTooltip: function (selector, msg, placement) {
        var elem;
        if (typeof placement === 'undefined') {
            placement = 'right'; // default to right-aligned tooltip
        }
        elem = $(selector);
        elem.tooltip({'title': msg, 'trigger': 'manual', 'placement': placement});
        elem.tooltip('show');
        elem.addClass('error');
        elem.on('focus click', function(e) {
            elem.removeClass('error');
            elem.tooltip('hide');
        });
    }
};

var FormHelpers = {
    validate: function (form, evt) {
        // Form validation for modal dialog
        var example_name = form.find('#example_name').val();
        var example_description = form.find('#example_description').val();
        if (!(example_name)) {
            evt.preventDefault();
            Utils.renderFieldErrorTooltip('#example_name', 'Name is required', 'right');
        }
        if (!(example_description)) {
            evt.preventDefault();
            Utils.renderFieldErrorTooltip('#example_description', 'Description is required', 'right');
        }
    },
    init: function () {
        var self = this;
        var example_form = $('#new-example-form');
        example_form.on('submit', function (evt) {
            self.validate(example_form, evt)
        });
    }
};

$(document).ready(function() {
    FormHelpers.init();
});
