"use strict";

define(['underscore', 'jquery', 'backbone', 'config'],
    function(_, $, Backbone, Config) {
        var Models = {};

        // Put your Backbone models and collections here.
        Models.Info = Backbone.Model.extend({
            urlRoot: Config.uri.api.info
        });

        Models.User = Backbone.Model.extend({
            urlRoot: Config.uri.api.users
        });

        Models.Group = Backbone.Model.extend({
            urlRoot: Config.uri.api.groups
        });

        Models.Users = Backbone.Collection.extend({
            url: Config.uri.api.users
        });

        Models.Groups = Backbone.Collection.extend({
            url: Config.uri.api.groups
        });

        return Models;
    }
);