"use strict";

define(['underscore', 'jquery', 'backbone', 'config'],
    function(_, $, Backbone, Config) {
        var Models = {};

        // Put your Backbone models and collections here.
        Models.Info = Backbone.Model.extend({
            urlRoot: Config.uri.api.info
        });

        return Models;
    }
);