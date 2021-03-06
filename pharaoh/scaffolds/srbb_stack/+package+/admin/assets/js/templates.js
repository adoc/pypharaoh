"use strict";

define(['underscore',
        text_url("user_dropdown.html.tmpl"),
        text_url("alert_dropdown.html.tmpl"),
        text_url("users_list_table_body.html.tmpl"),
        text_url("groups_list_table_body.html.tmpl"),
        text_url("message_dropdown.html.tmpl")],

    function(_,
            userDropdownTemplate,
            alertDropdownTemplate,
            usersListTableTemplate,
            groupsListTableTemplate,
            messagesDropdownTemplate) {

        var Templates = {};

        // Put your template pre-renders here.
        Templates.userDropdown = _.template(userDropdownTemplate);
        Templates.alertDropdown = _.template(alertDropdownTemplate);
        Templates.usersListTable = _.template(usersListTableTemplate);
        Templates.groupsListTable = _.template(groupsListTableTemplate);
        Templates.messagesDropdown = _.template(messagesDropdownTemplate);

        return Templates;
    }
);