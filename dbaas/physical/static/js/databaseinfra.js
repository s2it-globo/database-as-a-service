
var $ = django.jQuery;

var DatabaseInfra = function() {
    // this.engine_changed();
};

DatabaseInfra.prototype = {
    engine_changed: function() {
        this.update_components();
    },
    update_components: function() {
        this.update_endpoint();
        this.update_plans();
        this.clean_environment_options();
    },
    update_endpoint: function() {
        var engine_id = $("#id_engine").val() || "none";
        var engine_name = $('#id_engine :selected').text() || "none";

        if (engine_name.match(/mongo/g)) {
            this.hide_endpoint();
        } else {
            if (engine_id == "none") {
                this.hide_endpoint();
            } else {
                this.show_endpoint();
            };
        };
    },
    clean_plan_options: function() {
        $('#id_plan option:gt(0)').remove();
    },
    clean_environment_options: function() {
        $('#id_environment option:gt(0)').remove();
    },
    update_environments: function(initial_environment_id) {
        var first_environment_id = $("#id_environment").val() || "0";
        
        if (typeof initial_environment_id != "undefined") {
            first_environment_id = initial_environment_id
        }

        //remove options from plan, except the first one
        this.clean_environment_options();

        var plan_id = $("#id_plan").val() || "none";
        if (plan_id != "none") {
            
            $.ajax({
                "dataType": "json",
                "url": "/api/plan/" + plan_id + "/",
                "type": "GET",
            }).done(function(data) {
                if (data.error) {
                    alert(data.error);
                } else {
                    var environment = $("#id_environment");
                    $.each(data.environments, function(index, item) {
                        environment.append($("<option></option>").attr("value", item.id).text(item.name));
                        /* 
                        discover if it is the selected value. This is necessary in cases where the form is submited
                        but is returned with a validation error.
                        */
                        if (parseInt(item.id) == parseInt(first_environment_id)) {
                            environment.val(first_environment_id);
                        };
                    });
                };
            }).fail(function() {
                alert("invalid server response");
            });
        };
        
    },
    update_plans: function() {            
        var first_plan_id = $("#id_plan").val() || "0";
        var first_environment_id = $("#id_environment").val() || "0";
        //remove options from plan, except the first one
        this.clean_plan_options();

        var engine_id = $("#id_engine").val() || "none";
        if (engine_id != "none") {
            
            $.ajax({
                "dataType": "json",
                "url": "/api/plan/",
                "type": "GET",
                "data": { "engine_id": engine_id, },
            }).done(function(data) {
                if (data.error) {
                    alert(data.error);
                } else {
                    var plan = $("#id_plan");
                    $.each(data, function(index, item) {
                        plan.append($("<option></option>").attr("value", item.id).text(item.name));
                        /* 
                        discover if it is the selected value. This is necessary in cases where the form is submited
                        but is returned with a validation error.
                        */
                        if (parseInt(item.id) == parseInt(first_plan_id)) {
                            plan.val(first_plan_id);
                            plan.trigger("change", [first_environment_id]);
                        };
                    });
                    
                };
            }).fail(function() {
                alert("invalid server response");
            });
        };
        
    },
    hide_endpoint: function() {
        var engine_id = $("#id_engine").val() || "none";
        var engine_name = $('#id_engine :selected').text() || "none";
        // only hide if it is not mongo or if no engine is selected
        if ((engine_name.match(/mongo/g) || engine_id == "none" )) {
            var endpoint = $(".control-group.field-endpoint");
            if (endpoint.is(":visible")) {
                endpoint.hide();
            };
        };
    },
    show_endpoint: function() {
        var endpoint = $(".control-group.field-endpoint");
        if (! endpoint.is(":visible")) {
            endpoint.show();
        };
    },
};
