"use strict";

define(['underscore',
        text_url("user_dropdown.html.tmpl"),
        text_url("alert_dropdown.html.tmpl")],
    function(_,
            userDropdownTemplate,
            alertDropdownTemplate) {
        var Templates = {};

        // Put your template pre-renders here.
        Templates.userDropdown = _.template(userDropdownTemplate);
        Templates.alertDropdown = _.template(alertDropdownTemplate);

        return Templates;
    }
);