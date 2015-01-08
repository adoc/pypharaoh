"use strict";

define(['underscore',
        text_url("tmpl/home.html_tmpl")],
    function(_,
            homeTemplate) {
        Templates = {};

        // Put your template pre-renders here.
        Templates.Home = _.template(homeTemplate);

        return Templates;
    }
);