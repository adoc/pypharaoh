"use strict";

define(['underscore', 'jquery', 'backbone', 'config', 'models', 'templates'],
    function(_, $, Backbone, Config, Models, Templates) {
        var Views = {};


        var BaseView = Backbone.View.extend({
            Config: Config,
        });


        // Put your Backbone views here.
        Views.userDropdown = BaseView.extend({
            enable_profile: false,
            enable_messaging: false,
            enable_settings: false,
            el: $("#user_dropdown"),
            initialize: function (options) {
                this.infoModel = options['infoModel'];
                this.listenTo(this.infoModel, "change",
                                    _.debounce(this.render));
            },
            render: function () {
                this.$el.html(Templates.userDropdown(this));
            }
        });

        Views.alertDropdown = BaseView.extend({
            el: $("#alert_dropdown"),
            initialize: function (options) {
                this.infoModel = options['infoModel'];
                this.listenTo(this.infoModel, "change",
                                    _.debounce(this.render));
            },
            render: function () {
                this.$el.html(Templates.alertDropdown(this));
            }
        });

        Views.messageDropdown = BaseView.extend({
            el: $("#message_dropdown"),
            initialize: function (options) {
                this.infoModel = options['infoModel'];
                this.listenTo(this.infoModel, "change",
                                    _.debounce(this.render));
            },
            render: function () {
                this.$el.html(Templates.alertDropdown(this));
            }
        });


        return Views;
    }
);