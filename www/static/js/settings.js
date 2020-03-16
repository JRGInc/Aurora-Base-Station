// Author: Larry A. Hartman
// Company: Janus Research Group


function btn_clk_settings(button_name) {
    // - Called from 'settings.html/#div' submit buttons
    // - Collects data from 'settings.html/#div' control elements
    // - Posts collected data from 'settings.html/#div' control elements
    // - Gets values for 'settings.html#div' controls and populates


    var valid = true;
    var valid_int = true;
    var valid_time = true;
    var valid_url = true;
    var valid_ip = true;
    var valid_email = true;
    var valid_phone = true;
    var valid_eval = true;

    // Collect user updates from 'settings.html/#settings_(button_name)' control elements
    switch (button_name) {
        case 'core':
            var post_data = {
                button_name: button_name,
                sysname: txt_settings_core_sysname.value,
                customerid: txt_settings_core_customerid.value
            };
            break;

        case 'temp':
            var post_data = {
                button_name: button_name,
                unit: radio_value(rad_settings_dataunits_temp)
            };
            break;

        case 'press':
            var post_data = {
                button_name: button_name,
                unit: radio_value(rad_settings_dataunits_press)
            };
            break;

        case 'log':
            var post_data = {
                button_name: button_name,
                activity: radio_value(rad_settings_log_activity),
                janusess: radio_value(rad_settings_log_janusess),
                command: radio_value(rad_settings_log_command),
                conversion: radio_value(rad_settings_log_conversion),
                heartbeat: radio_value(rad_settings_log_heartbeat),
                interface: radio_value(rad_settings_log_interface),
                polling: radio_value(rad_settings_log_polling),
                server: radio_value(rad_settings_log_server),
                setup: radio_value(rad_settings_log_setup),
                tasks: radio_value(rad_settings_log_tasks)
            };
            break;

        case 'compact':
            var time_raw = txt_settings_compact_firsttime.value;
            var interval_raw = nbr_settings_compact_interval.value;

            valid_time = validate_time(txt_settings_compact_firsttime, time_raw);
            valid_int = validate_int(nbr_settings_compact_interval, interval_raw, 'interval');

            if (valid_time && valid_int) {

                interval_int = parseInt(nbr_settings_compact_interval.value, 10);

                if ((interval_int < 1) || (interval_int > 24)) {
                    nbr_settings_compact_interval.classList.remove('alert-info');
                    nbr_settings_compact_interval.classList.add('alert-warning');
                    nbr_settings_compact_interval.classList.add('text-danger');
                    invalid_alert('Given interval is outside physical limits: 1 to 24!');
                    valid_eval = false;
                };

                if (valid_eval) {
                    var post_data = {
                        button_name: button_name,
                        dbcompact_firsttime: txt_settings_compact_firsttime.value,
                        dbcompact_interval: interval_int,
                    };
                } else {
                    valid = false;
                };

            } else {
                valid = false;
            };

            break;

        case 'update':
            var time_raw = txt_settings_update_firsttime.value;
            var interval_raw = nbr_settings_update_interval.value;

            valid_time = validate_time(txt_settings_update_firsttime, time_raw);
            valid_int = validate_int(nbr_settings_update_interval, interval_raw, 'interval');

            if (valid_time && valid_int) {

                interval_int = parseInt(nbr_settings_update_interval.value, 10);

                if ((interval_int < 1) || (interval_int > 24)) {
                    nbr_settings_update_interval.classList.remove('alert-info');
                    nbr_settings_update_interval.classList.add('alert-warning');
                    nbr_settings_update_interval.classList.add('text-danger');
                    invalid_alert('Given interval is outside physical limits: 1 to 24!');
                    valid_eval = false;
                };

                if (valid_eval) {
                    var post_data = {
                        button_name: button_name,
                        updateemail_firsttime: txt_settings_update_firsttime.value,
                        updateemail_interval: interval_int,
                    };
                } else {
                    valid = false;
                };

            } else {
                valid = false;
            };

            break;

        case 'cloud':
            var url_raw = txt_settings_cloud_url.value;

            valid_url = validate_url(txt_settings_cloud_url, url_raw, "cloud server");

            if (valid_url) {
                var post_data = {
                    button_name: button_name,
                    enable: chk_settings_cloud_en.checked,
                    url: txt_settings_cloud_url.value,
                };
            } else {
                valid = false;
            };

            break;

        case 'network':
            var url_raw = txt_settings_network_url.value;
            var int_good_raw = nbr_settings_network_intgood.value;
            var int_bad_raw = nbr_settings_network_intbad.value;
            var timeout_raw = nbr_settings_network_timeout.value;

            valid_url = validate_url(txt_settings_network_url, url_raw, "network server");
            if (!validate_int(nbr_settings_network_intgood, int_good_raw, 'successful check interval')) {
                valid_int = false;
            };
            if (!validate_int(nbr_settings_network_intbad, int_bad_raw, 'unsuccessful check interval')) {
                valid_int = false;
            };
            if (!validate_int(nbr_settings_network_timeout, timeout_raw, 'timeout')) {
                valid_int = false;
            };

            if (valid_url && valid_int) {

                var int_good_int = parseInt(nbr_settings_network_intgood.value, 10);
                var int_bad_int = parseInt(nbr_settings_network_intbad.value, 10);
                var timeout_int = parseInt(nbr_settings_network_timeout.value, 10);

                if ((int_good_int < 1) || (int_good_int > 60)) {
                    valid_eval = false;
                    nbr_settings_network_intgood.classList.remove('alert-info');
                    nbr_settings_network_intgood.classList.add('alert-warning');
                    nbr_settings_network_intgood.classList.add('text-danger');
                    invalid_alert('Interval is outside allowable range!');
                };
                if ((int_bad_int < 1) || (int_bad_int > 60)) {
                    valid_eval = false;
                    nbr_settings_network_intbad.classList.remove('alert-info');
                    nbr_settings_network_intbad.classList.add('alert-warning');
                    nbr_settings_network_intbad.classList.add('text-danger');
                    invalid_alert('Interval is outside allowable range!');
                };
                if (int_bad_int > int_good_int) {
                    valid_eval = false;
                    nbr_settings_network_intbad.classList.remove('alert-info');
                    nbr_settings_network_intbad.classList.add('alert-warning');
                    nbr_settings_network_intbad.classList.add('text-danger');
                    invalid_alert('Unsuccessful check interval must be less than or equal to successful check interval!');
                };
                if (timeout_int <= 0) {
                    valid_eval = false;
                    nbr_settings_network_timeout.classList.remove('alert-info');
                    nbr_settings_network_timeout.classList.add('alert-warning');
                    nbr_settings_network_timeout.classList.add('text-danger');
                    invalid_alert('Timeout must be at least 1 second!');
                };

                if (valid_eval) {
                    var post_data = {
                        button_name: button_name,
                        url_server: txt_settings_network_url.value,
                        interval_good: int_good_int,
                        interval_bad: int_bad_int,
                        url_timeout: timeout_int,
                    };

                } else {
                    valid = false;
                };
            }else {
                valid = false;
            };

            break;

        case 'email':
            var url_raw = txt_settings_smtp_server.value;
            var port_raw = nbr_settings_smtp_port.value;
            var timeout_raw = nbr_settings_smtp_timeout.value;
            var email_raw = txt_settings_smtp_from.value;

            valid_url = validate_url(txt_settings_smtp_server, url_raw, "network server");
            if (!validate_int(nbr_settings_smtp_port, port_raw, 'port')) {
                valid_int = false;
            };
            if (!validate_int(nbr_settings_smtp_timeout, timeout_raw, 'timeout')) {
                valid_int = false;
            };
            valid_email = validate_email(txt_settings_smtp_from, email_raw);

            if (valid_url && valid_int && valid_email) {

                var port_int = parseInt(nbr_settings_smtp_port.value, 10);
                var timeout_int = parseInt(nbr_settings_smtp_timeout.value, 10);

                if (port_int <= 0) {
                    valid_eval = false;
                    nbr_settings_smtp_port.classList.remove('alert-info');
                    nbr_settings_smtp_port.classList.add('alert-warning');
                    nbr_settings_smtp_port.classList.add('text-danger');
                    invalid_alert('Port number must be at least 1!');
                };
                if (timeout_int <= 0) {
                    valid_eval = false;
                    nbr_settings_smtp_timeout.classList.remove('alert-info');
                    nbr_settings_smtp_timeout.classList.add('alert-warning');
                    nbr_settings_smtp_timeout.classList.add('text-danger');
                    invalid_alert('Timeout must be at least 1 second!');
                };

                if (valid_eval) {
                    var post_data = {
                        button_name: button_name,
                        smtp_enable: chk_settings_smtp_en.checked,
                        smtp_from: txt_settings_smtp_from.value,
                        smtp_server: txt_settings_smtp_server.value,
                        smtp_port: port_int,
                        smtp_timeout: timeout_int,
                        smtp_password: pwd_settings_smtp_pwd.value
                    };

                } else {
                    valid = false;
                };
            } else {
                valid = false;
            };

            break;

        case 'email_list':
            var email_raw = txt_settings_smtp_address.value;

            valid_email = validate_email(txt_settings_smtp_address, email_raw);

            if (valid_email) {
                var post_data = {
                    button_name: button_name,
                    smtp_address: txt_settings_smtp_address.value,
                    smtp_list: radio_value(rad_settings_smtp_list),
                    smtp_choice: radio_value(rad_settings_smtp_choice)
                };

            } else {
                valid = false;
            };
            break;

        case 'sms':
            var post_data = {
                button_name: button_name,
                sms_enable: chk_settings_sms_en.checked
            };
            break;

        case 'sms_list':
            var phone_raw = txt_settings_sms_mobile.value;

            valid_phone = validate_phone(txt_settings_sms_mobile, phone_raw);

            if (btn_settings_sms_gateways.value == '') {
                invalid_alert('Must make a selection from drop-down menu!');
            }

            if (valid_phone && (btn_settings_sms_gateways.value != '')) {

                sms_mobile_raw = txt_settings_sms_mobile.value;
                sms_mobile_no_paren = sms_mobile_raw.replace(/[()]/g, "");
                sms_mobile_no_dash = sms_mobile_no_paren.replace(/-/g, "");
                sms_mobile_no_dot = sms_mobile_no_dash.replace(/\./g, "");
                sms_mobile_conditioned = sms_mobile_no_dot.replace(/\s+/g, "");

                var post_data = {
                    button_name: button_name,
                    sms_mobile: sms_mobile_conditioned,
                    sms_list: radio_value(rad_settings_sms_list),
                    sms_gateway: btn_settings_sms_gateways.value
                };
            } else {
                valid = false;
            };
            break;

        case 'snmp':
            var server_raw = txt_settings_snmp_server.value;
            var port_raw = nbr_settings_snmp_port.value;

            valid_ip = validate_ip(txt_settings_snmp_server, server_raw);
            valid_int = validate_int(nbr_settings_snmp_port, port_raw, 'port');

            if (valid_ip && valid_int) {

                var port_int = parseInt(nbr_settings_snmp_port.value, 10);

                if (port_int <= 0) {
                    valid_eval = false;
                    nbr_settings_snmp_port.classList.remove('alert-info');
                    nbr_settings_snmp_port.classList.add('alert-warning');
                    nbr_settings_snmp_port.classList.add('text-danger');
                    invalid_alert('Port number must be at least 1!');
                };

                if (valid_eval) {
                    var post_data = {
                        button_name: button_name,
                        agent_enable: chk_settings_snmp_agent_en.checked,
                        notify_enable: chk_settings_snmp_notify_en.checked,
                        server: txt_settings_snmp_server.value,
                        port: port_int,
                        community:txt_settings_snmp_comm.value
                    };
                } else {
                    valid = false;
                };

            } else {
                valid = false;
            };

            break;
    };

    // AJAX call to post collected data and return updated values from server
    if (valid) {
        $.ajax({
            url: '/',
            dataType: 'json',
            data: JSON.stringify(post_data),
            type: "POST",
            success: function ( data ) {
                switch (button_name) {
                    case 'core':
                        // Update document/head and navbar titles
                        update_titles(data);

                        // Update values in 'settings_core' controls
                        update_settings_core(data);
                        update_alert('System values successfully updated!');
                        break;

                    case 'temp':
                        // Update values in 'settings_dataunits' controls
                        update_settings_dataunits(data);
                        update_alert('Temperature units successfully updated!');
                        break

                    case 'press':
                        // Update values in 'settings_dataunits' controls
                        update_settings_dataunits(data);
                        update_alert('Pressure units successfully updated!');
                        break;

                    case 'log':
                        // Update values in 'settings_log' controls
                        update_settings_log(data);
                        update_alert('Log settings successfully updated!');
                        break;

                    case 'compact':
                        // Update values in 'settings_compact' controls
                        update_settings_compact(data);
                        update_alert('Database compact settings successfully updated!');
                        break;

                    case 'update':
                        // Update values in 'settings_update' controls
                        update_settings_update(data);
                        update_alert('Status update settings successfully updated!');
                        break;

                    case 'cloud':
                        // Update values in 'settings_cloud' controls
                        update_settings_cloud(data);
                        update_alert('Cloud settings successfully updated!');
                        break;

                    case 'network':
                        // Update values in 'settings_network' controls
                        update_settings_network(data);
                        update_alert('Network check settings successfully updated!');
                        break;

                    case 'email':
                        // Update values in 'settings_email' controls
                        update_settings_email(data);
                        update_alert('Email settings successfully updated!');
                        break;

                    case 'email_list':
                        // Update values in 'settings_email' controls
                        update_settings_email_list(data);
                        update_alert('Email lists successfully updated!');
                        break;

                    case 'sms':
                        // Update values in 'settings_sms' controls
                        update_settings_sms(data);
                        update_alert('SMS settings successfully updated!');
                        break;

                    case 'sms_list':
                        // Update values in 'settings_sms' controls
                        update_settings_sms_list(data);
                        update_alert('SMS lists successfully updated!');
                        break;

                    case 'snmp':
                        // Update values in 'settings_snmp' controls
                        update_settings_snmp(data);
                        update_alert('SNMP settings successfully updated!');
                        break;

                };
            },
        });
    };
};


function lbl_clk_settings_dataunits_temp_toggle(selection) {
    // - Called from 'settings.html/#settings_dataunits'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_dataunits_temp' elements
    // Add 'active' class to 'lbl_settings_dataunits#_temp'
    // Set property 'checked' on 'rad_settings_dataunits#_temp'
    remove_class(els_lbl_settings_dataunits_temp, 'active');
    ids_lbl_settings_dataunits_temp[selection].classList.add('active');
    ids_rad_settings_dataunits_temp[selection].checked = true;
    add_class(els_lbl_settings_dataunits_temp, 'alert-info');
    ids_lbl_settings_dataunits_temp[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_dataunits_temp, 'btn_primary');
    ids_lbl_settings_dataunits_temp[selection].classList.add('btn-primary');
};


function lbl_clk_settings_dataunits_press_toggle(selection) {
    // - Called from 'settings.html/#settings_dataunits'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_dataunits_press' elements
    // Add 'active' class to 'lbl_settings_dataunits#_press'
    // Set property 'checked' on 'rad_settings_dataunits#_press'
    remove_class(els_lbl_settings_dataunits_press, 'active');
    ids_lbl_settings_dataunits_press[selection].classList.add('active');
    ids_rad_settings_dataunits_press[selection].checked = true;
    add_class(els_lbl_settings_dataunits_press, 'alert-info');
    ids_lbl_settings_dataunits_press[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_dataunits_press, 'btn_primary');
    ids_lbl_settings_dataunits_press[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_activity_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_activity' elements
    // Add 'active' class to 'lbl_settings_log#_activity'
    // Set property 'checked' on 'rad_settings_log#_activity'
    remove_class(els_lbl_settings_log_activity, 'active');
    ids_lbl_settings_log_activity[selection].classList.add('active');
    ids_rad_settings_log_activity[selection].checked = true;
    add_class(els_lbl_settings_log_activity, 'alert-info');
    ids_lbl_settings_log_activity[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_activity, 'btn_primary');
    ids_lbl_settings_log_activity[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_janusess_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_janusess' elements
    // Add 'active' class to 'lbl_settings_log#_janusess'
    // Set property 'checked' on 'rad_settings_log#_janusess'
    remove_class(els_lbl_settings_log_janusess, 'active');
    ids_lbl_settings_log_janusess[selection].classList.add('active');
    ids_rad_settings_log_janusess[selection].checked = true;
    add_class(els_lbl_settings_log_janusess, 'alert-info');
    ids_lbl_settings_log_janusess[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_janusess, 'btn_primary');
    ids_lbl_settings_log_janusess[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_command_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_command' elements
    // Add 'active' class to 'lbl_settings_log#_command'
    // Set property 'checked' on 'rad_settings_log#_command'
    remove_class(els_lbl_settings_log_command, 'active');
    ids_lbl_settings_log_command[selection].classList.add('active');
    ids_rad_settings_log_command[selection].checked = true;
    add_class(els_lbl_settings_log_command, 'alert-info');
    ids_lbl_settings_log_command[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_command, 'btn_primary');
    ids_lbl_settings_log_command[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_conversion_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_conversion' elements
    // Add 'active' class to 'lbl_settings_log#_conversion'
    // Set property 'checked' on 'rad_settings_log#_conversion'
    remove_class(els_lbl_settings_log_conversion, 'active');
    ids_lbl_settings_log_conversion[selection].classList.add('active');
    ids_rad_settings_log_conversion[selection].checked = true;
    add_class(els_lbl_settings_log_conversion, 'alert-info');
    ids_lbl_settings_log_conversion[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_conversion, 'btn_primary');
    ids_lbl_settings_log_conversion[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_heartbeat_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_heartbeat' elements
    // Add 'active' class to 'lbl_settings_log#_heartbeat'
    // Set property 'checked' on 'rad_settings_log#_heartbeat'
    remove_class(els_lbl_settings_log_heartbeat, 'active');
    ids_lbl_settings_log_heartbeat[selection].classList.add('active');
    ids_rad_settings_log_heartbeat[selection].checked = true;
    add_class(els_lbl_settings_log_heartbeat, 'alert-info');
    ids_lbl_settings_log_heartbeat[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_heartbeat, 'btn_primary');
    ids_lbl_settings_log_heartbeat[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_interface_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_interface' elements
    // Add 'active' class to 'lbl_settings_log#_interface'
    // Set property 'checked' on 'rad_settings_log#_interface'
    remove_class(els_lbl_settings_log_interface, 'active');
    ids_lbl_settings_log_interface[selection].classList.add('active');
    ids_rad_settings_log_interface[selection].checked = true;
    add_class(els_lbl_settings_log_interface, 'alert-info');
    ids_lbl_settings_log_interface[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_interface, 'btn_primary');
    ids_lbl_settings_log_interface[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_polling_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_polling' elements
    // Add 'active' class to 'lbl_settings_log#_polling'
    // Set property 'checked' on 'rad_settings_log#_polling'
    remove_class(els_lbl_settings_log_polling, 'active');
    ids_lbl_settings_log_polling[selection].classList.add('active');
    ids_rad_settings_log_polling[selection].checked = true;
    add_class(els_lbl_settings_log_polling, 'alert-info');
    ids_lbl_settings_log_polling[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_polling, 'btn_primary');
    ids_lbl_settings_log_polling[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_server_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_server' elements
    // Add 'active' class to 'lbl_settings_log#_server'
    // Set property 'checked' on 'rad_settings_log#_server'
    remove_class(els_lbl_settings_log_server, 'active');
    ids_lbl_settings_log_server[selection].classList.add('active');
    ids_rad_settings_log_server[selection].checked = true;
    add_class(els_lbl_settings_log_server, 'alert-info');
    ids_lbl_settings_log_server[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_server, 'btn_primary');
    ids_lbl_settings_log_server[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_setup_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_setup' elements
    // Add 'active' class to 'lbl_settings_log#_setup'
    // Set property 'checked' on 'rad_settings_log#_setup'
    remove_class(els_lbl_settings_log_setup, 'active');
    ids_lbl_settings_log_setup[selection].classList.add('active');
    ids_rad_settings_log_setup[selection].checked = true;
    add_class(els_lbl_settings_log_setup, 'alert-info');
    ids_lbl_settings_log_setup[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_setup, 'btn_primary');
    ids_lbl_settings_log_setup[selection].classList.add('btn-primary');
};


function lbl_clk_settings_log_tasks_toggle(selection) {
    // - Called from 'settings.html/#settings_log'
    // - Toggles associated button value and styles


    // Remove 'active' class from 'cls_fm_lbl_settings_log_tasks' elements
    // Add 'active' class to 'lbl_settings_log#_tasks'
    // Set property 'checked' on 'rad_settings_log#_tasks'
    remove_class(els_lbl_settings_log_tasks, 'active');
    ids_lbl_settings_log_tasks[selection].classList.add('active');
    ids_rad_settings_log_tasks[selection].checked = true;
    add_class(els_lbl_settings_log_tasks, 'alert-info');
    ids_lbl_settings_log_tasks[selection].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_tasks, 'btn_primary');
    ids_lbl_settings_log_tasks[selection].classList.add('btn-primary');
};


function chk_clk_settings_cloud_en_toggle() {
    // - Called from 'settings.html/#settings_cloud' cloud en checkbox
    // - Toggles associated button value and styles


    // Determines state of checkbox and executes appropriate toggles
    if (chk_settings_cloud_en.checked == true) {
        btn_settings_cloud_en.classList.remove('btn-danger');
        btn_settings_cloud_en.classList.add('alert-danger');
        btn_settings_cloud_en.value = 'Cloud Enabled';
        txt_settings_cloud_url.disabled = false;
        txt_settings_cloud_url.classList.remove('alert-secondary');
        txt_settings_cloud_url.classList.add('alert-info');
    } else {
        btn_settings_cloud_en.classList.remove('alert-danger');
        btn_settings_cloud_en.classList.add('btn-danger');
        btn_settings_cloud_en.value = 'Cloud Disabled';
        txt_settings_cloud_url.disabled = true;
        txt_settings_cloud_url.classList.remove('alert-info');
        txt_settings_cloud_url.classList.add('alert-secondary');
    };
};


function chk_clk_settings_smtp_en_toggle() {
    // - Called from 'settings.html/#settings_email' cloud en checkbox
    // - Toggles associated button value and styles


    // Determines state of checkbox and executes appropriate toggles
    if (chk_settings_smtp_en.checked == true) {
        btn_settings_smtp_en.classList.remove('btn-danger');
        btn_settings_smtp_en.classList.add('alert-danger');
        btn_settings_smtp_en.value = 'Email Enabled';
        txt_settings_smtp_from.disabled = false;
        txt_settings_smtp_server.disabled = false;
        nbr_settings_smtp_port.disabled = false;
        nbr_settings_smtp_timeout.disabled = false;
        pwd_settings_smtp_pwd.disabled = false;
        remove_class(els_settings_smtp, 'alert-secondary');
        add_class(els_settings_smtp, 'alert-info');
    } else {
        btn_settings_smtp_en.classList.remove('alert-danger');
        btn_settings_smtp_en.classList.add('btn-danger');
        btn_settings_smtp_en.value = 'Email Disabled';
        txt_settings_smtp_from.disabled = true;
        txt_settings_smtp_server.disabled = true;
        nbr_settings_smtp_port.disabled = true;
        nbr_settings_smtp_timeout.disabled = true;
        pwd_settings_smtp_pwd.disabled = true;
        remove_class(els_settings_smtp, 'alert-info');
        add_class(els_settings_smtp, 'alert-secondary');
    };
};


function lbl_clk_settings_smtp_list_toggle(list) {
    // - Called from 'settings.html/#settings_email' cloud en checkbox
    // - Toggles associated button value and styles


    // Remove 'active' class from 'els_lbl_settings_smtp_list' controls
    // Add 'alert-info' class from 'els_lbl_settings_smtp_list' controls
    // Set property 'checked' on 'rad_settings_smtp0_list'
    // Toggle 'active' class on 'lbl_settings_smtp0_list'
    remove_class(els_lbl_settings_smtp_list, 'active');
    add_class(els_lbl_settings_smtp_list, 'alert-info');
    remove_class(els_lbl_settings_smtp_list, 'btn-primary');
    ids_rad_settings_smtp_list[list].checked = true;
    ids_lbl_settings_smtp_list[list].classList.add('active');
    ids_lbl_settings_smtp_list[list].classList.remove('alert-info');
    ids_lbl_settings_smtp_list[list].classList.add('btn-primary');

    // Set 'btn_settings_smtp_list' value
    btn_settings_smtp_list.value = 'Modify ' + list[0].toUpperCase() + list.substr(1) + ' Email List';

};


function lbl_clk_settings_smtp_choice_toggle(choice) {
    // - Called from 'settings.html/#settings_email' cloud en checkbox
    // - Toggles associated button value and styles


    // Remove 'active' class from 'els_lbl_settings_smtp_choice' controls
    // Add 'alert-info' class from 'els_lbl_settings_smtp_choice' controls
    // Set property 'checked' on 'rad_settings_smtp0_choice'
    // Toggle 'active' class on 'lbl_settings_smtp0_choice'
    remove_class(els_lbl_settings_smtp_choice, 'active');
    add_class(els_lbl_settings_smtp_choice, 'alert-info');
    remove_class(els_lbl_settings_smtp_choice, 'btn-primary');
    ids_rad_settings_smtp_choice[choice].checked = true;
    ids_lbl_settings_smtp_choice[choice].classList.add('active');
    ids_lbl_settings_smtp_choice[choice].classList.remove('alert-info');
    ids_lbl_settings_smtp_choice[choice].classList.add('btn-primary');
};


function chk_clk_settings_sms_en_toggle() {
    // - Called from 'settings.html/#settings_sms' cloud en checkbox
    // - Toggles associated button value and styles


    // Determines state of checkbox and executes appropriate toggles
    if (chk_settings_sms_en.checked == true) {
        btn_settings_sms_en.classList.remove('btn-danger');
        btn_settings_sms_en.classList.add('alert-danger');
        btn_settings_sms_en.value = 'SMS Enabled';
    } else {
        btn_settings_sms_en.classList.remove('alert-danger');
        btn_settings_sms_en.classList.add('btn-danger');
        btn_settings_sms_en.value = 'SMS Disabled';
    };
};


function a_clk_dm_settings_sms_gateways_toggle(selection, setting) {
    // - Called from 'settings.html/#settings_messaging' sms dropdown menu items
    // - Gets selection and sets dropdown button to active state


    btn_settings_sms_gateways.innerHTML = selection;
    btn_settings_sms_gateways.classList.add('active');
    btn_settings_sms_gateways.value = setting;
};


function lbl_clk_settings_sms_list_toggle(list) {
    // - Called from 'settings.html/#settings_sms' cloud en checkbox
    // - Toggles associated button value and styles


    // Remove 'active' class from 'btn_settings_sms_gateways'
    // Remove 'active' class from 'els_lbl_settings_sms_list' controls
    // Add 'alert-info' class from 'els_lbl_settings_sms_list' controls
    // Set property 'checked' on 'rad_settings_sms0_list'
    // Toggle 'active' class on 'lbl_settings_sms0_list'
    remove_class(els_lbl_settings_sms_list, 'active');
    add_class(els_lbl_settings_sms_list, 'alert-info');
    ids_rad_settings_sms_list[list].checked = true;
    ids_lbl_settings_sms_list[list].classList.add('active');
    ids_lbl_settings_sms_list[list].classList.remove('alert-info');
    ids_lbl_settings_sms_list[list].classList.add('btn-primary');

    // Set 'btn_settings_smtp_list' value
    btn_settings_smtp_list.value = 'Modify ' + list[0].toUpperCase() + list.substr(1) + ' SMS List';
};


function chk_clk_settings_snmp_agent_en_toggle() {
    // - Called from 'settings.html/#settings_snmp' cloud en checkbox
    // - Toggles associated button value and styles


    // Determines state of checkbox and executes appropriate toggles
    if (chk_settings_snmp_agent_en.checked == true) {
        btn_settings_snmp_agent_en.classList.remove('btn-danger');
        btn_settings_snmp_agent_en.classList.add('alert-danger');
        btn_settings_snmp_agent_en.value = 'SNMP Agent Enabled';
    } else {
        btn_settings_snmp_agent_en.classList.remove('alert-danger');
        btn_settings_snmp_agent_en.classList.add('btn-danger');
        btn_settings_snmp_agent_en.value = 'SNMP Agent Disabled';
    };
};


function chk_clk_settings_snmp_notify_en_toggle() {
    // - Called from 'settings.html/#settings_snmp' cloud en checkbox
    // - Toggles associated button value and styles


    // Determines state of checkbox and executes appropriate toggles
    if (chk_settings_snmp_notify_en.checked == true) {
        btn_settings_snmp_notify_en.classList.remove('btn-danger');
        btn_settings_snmp_notify_en.classList.add('alert-danger');
        btn_settings_snmp_notify_en.value = 'SNMP Notify Enabled';
        remove_class(els_settings_snmp_notify, 'alert-secondary');
        add_class(els_settings_snmp_notify, 'alert-info');
        txt_settings_snmp_server.disabled = false;
        nbr_settings_snmp_port.disabled = false;
        txt_settings_snmp_comm.disabled = false;
    } else {
        btn_settings_snmp_notify_en.classList.remove('alert-danger');
        btn_settings_snmp_notify_en.classList.add('btn-danger');
        btn_settings_snmp_notify_en.value = 'SNMP Notify Disabled';

        remove_class(els_settings_snmp_notify, 'alert-info');
        add_class(els_settings_snmp_notify, 'alert-secondary');
        txt_settings_snmp_server.disabled = true;
        nbr_settings_snmp_port.disabled = true;
        txt_settings_snmp_comm.disabled = true;
    };
};