// Author: Larry A. Hartman
// Company: Janus Research Group


// Set global variables
var stat_lvl = {
    'op': 0,
    's_evt': 1,
    'op_evt': 2,
    'op_err': 3,
    'crit': 4,
    'not_cfg': 5,
    'cfg_err': 6,
    'undeter': 7,
    'not_trk': 8
};

var status_messages = [
    "Operational",
    "Sensor Event",
    "Operational Event",
    "Operational Error",
    "Critical Error",
    "Not Setup",
    "Configuration Error",
    "Undetermined",
    "Not Tracked"
];

var status_bg_class = [
    'bg-success',
    'bg-magenta',
    'bg-primary',
    'bg-warning',
    'bg-danger',
    'bg-primary',
    'bg-warning',
    'bg-light',
    'bg-black'
];

var status_text_class = [
    'text-warning',
    'text-white',
    'text-white',
    'text-danger',
    'text-warning',
    'text-white',
    'text-success',
    'text-primary',
    'text-white'
];

var status_symbols = [
    '<i class="fas fa-check"></i>',
    '<i class="fas fa-check"></i>',
    '<i class="fas fa-exclamation"></i>',
    '<i class="fas fa-bolt"></i>',
    '<i class="fas fa-bomb"></i>',
    '<i class="fas fa-ban"></i>',
    '<i class="fas fa-exclamation"></i>',
    '<i class="fas fa-times"></i>',
    '<i class="fas fa-question"></i>'
];


// Update element attributes functions

function remove_status_classes(el_id) {
    // - Called from 'heartbeat.js/functions'
    // - Removes class names to given ids to indicate status

    if (el_id.classList.contains('table-secondary') == true) {
        el_id.classList.remove('table-secondary');
    };
    for (status = stat_lvl['op']; status <= stat_lvl['not_trk']; status++) {
        if (el_id.classList.contains(status_bg_class[status]) == true) {
            el_id.classList.remove(status_bg_class[status]);
        };
        if (el_id.classList.contains(status_text_class[status]) == true) {
            el_id.classList.remove(status_text_class[status]);
        };
    };
};


function add_status_classes(status, el_id) {
    // - Called from 'heartbeat.js/functions'
    // - Called from 'chan_modules.js/channel_module_carousel()'
    // - Adds class names to given ids to indicate status

    status = parseInt(status, 10);
    el_id.classList.add(status_bg_class[status]);
    el_id.classList.add(status_text_class[status]);
};

function remove_elements(el_id) {
    // - Called from 'sidebar_channels.js'
    // - Removes all elements from a given id

    // Remove element
    $(el_id).empty();
};


function add_class(el_arr, cls_name) {
    // - Called from 'settings.js'
    // - Adds a class from an array of elements


    // Cycle through element array
    // Remove class name
    for (var index = 0; index < el_arr.length; index++) {
        el_arr[index].classList.add(cls_name);
    };
};


function remove_class(el_arr, cls_name) {
    // - Called from 'navbar.js'
    // - Called from 'sidebar_settings.js'
    // - Called from 'sidebar_channels.js'
    // - Removes a class from an array of elements


    // Cycle through element array
    // Remove class name
    for (var index = 0; index < el_arr.length; index++) {
        el_arr[index].classList.remove(cls_name);
    };
};


function disp_none(el_arr) {
    // - Called from 'setup.js'
    // - Called from 'navbar.js'
    // - Called from 'sidebar_settings.js'
    // - Called from 'sidebar_channels.js'
    // - Sets display style to none


    // Cycle through element array
    // Set element display style to 'none'
    for (var index = 0; index < el_arr.length; index++) {
        el_arr[index].classList.remove('d-block');
        el_arr[index].classList.remove('d-inline');
        el_arr[index].classList.add('d-none');
    };
};


function disp_block(el_arr) {
    // - Called from 'sidebar_channels.js'
    // - Sets display style to block


    // Cycle through element array
    // Set element display style to 'none'
    for (var index = 0; index < el_arr.length; index++) {
        el_arr[index].classList.add('d-none');
        el_arr[index].classList.add('d-block');
    };
};

function disp_inline(el_arr) {
    // - Called from 'sidebar_channels.js'
    // - Sets display style to block


    // Cycle through element array
    // Set element display style to 'none'
    for (var index = 0; index < el_arr.length; index++) {
        el_arr[index].classList.add('d-none');
        el_arr[index].classList.add('d-inline');
    };
};


function radio_value(name_arr) {
    // - Called from 'setup.js'
    // - Called from 'settings.js'
    // - Gets checked radio button name


    // Cycle through name array until checked radio button is found
    // Return name of found radio button
    for (var index = 0; index < name_arr.length; index++) {
        if (name_arr[index].checked) {
            var value = name_arr[index].value;
            break;
        };
    };
    return value;
};


// This section focuses on user input validation


function invalid_alert(message) {
    // - Called from 'settings.js'
    // - Called from 'utilities.js'
    // - Called from 'settings.js'

    $.alert({
        title: 'Invalid User Input',
        content: String(message),
        buttons: {
            ok: {
                btnClass: 'btn-danger text-warning'
            }
        }
    });
};


function update_alert(message) {
    // - Called from 'settings.js'
    // - Called from 'utilities.js'
    // - Called from 'settings.js'

    $.alert({
        title: 'Successful Update',
        content: String(message),
        buttons: {
            ok: {
                btnClass: 'btn-success text-warning'
            }
        }
    });
};


function command_acknowledge(message) {
    // - Called from 'chan_setup.js'
    // - Called from 'chan_poll.js'

    $.alert({
        title: 'Command Acknowledged',
        content: String(message),
        buttons: {
            ok: {
                btnClass: 'btn-primary text-white'
            }
        }
    });
};


function sensor_low_alert(message) {
    // - Called from 'heartbeat.js'

    $.alert({
        title: 'Sensor Low Value',
        content: String(message),
        buttons: {
            ok: {
                btnClass: 'btn-primary text-white'
            }
        }
    });
};


function sensor_high_alert(message) {
    // - Called from 'heartbeat.js'

    $.alert({
        title: 'Sensor High Value',
        content: String(message),
        buttons: {
            ok: {
                btnClass: 'btn-danger text-warning'
            }
        }
    });
};


function validate_nbr(el_id, input, descr) {
    // - Called from 'settings.js'
    // - Validates input for number

    if (isNaN(input) || (input == '')) {
        el_id.classList.remove('alert-info');
        el_id.classList.add('alert-warning');
        el_id.classList.add('text-danger');
        invalid_alert('Given ' + descr + ' is not a number!');
        return false;
    } else {
        return true;
    };
};


function validate_int(el_id, input, descr) {
    // - Called from 'settings.js'
    // - Validated input for integer

    var valid_nbr = validate_nbr(el_id, input, descr);

    if (!valid_nbr) {
        return false;
    } else {
        if (!Number.isInteger(Number(input))) {
            el_id.classList.remove('alert-info');
            el_id.classList.add('alert-warning');
            el_id.classList.add('text-danger');
            invalid_alert('Given ' + descr + ' is not an integer!');
            return false;
        } else {
            return true;
        };
    };
};


function validate_time(el_id, input) {
    // - Called from 'settings.js'
    // - Validates input for time


    if ((input.search(":") == 1) || (input.search(":") == 2)) {
        var hour_raw = input.split(":")[0];
        var minute_raw = input.split(":")[1];

        var valid_int = validate_int(txt_settings_compact_firsttime, hour_raw, 'hour');
        if (!valid_int) {
            return false;
        } else {
            valid_int = validate_int(txt_settings_compact_firsttime, minute_raw, 'minute');
            if (!valid_int) {
                return false;
            } else {
                hour_int = parseInt(hour_raw, 10);
                minute_int = parseInt(minute_raw, 10);

                if ((hour_int < 0) || (hour_int > 23) || (minute_int < 0) || (minute_int > 59)) {
                    el_id.classList.remove('alert-info');
                    el_id.classList.add('alert-warning');
                    el_id.classList.add('text-danger');
                    invalid_alert('Given time is outside physical limits: hour (0 to 23) and minute (0 to 59)!');
                    return false;
                } else {
                    return true;
                };
            };
        };
    } else {
        el_id.classList.remove('alert-info');
        el_id.classList.add('alert-warning');
        el_id.classList.add('text-danger');
        invalid_alert('Given time is invalid!');
        return false;
    };
};


function validate_url(el_id, input, descr) {
    // - Called from 'settings.js'
    // - Validates input for url

    if ((input.search("http://") == 0) || (input.search("https://") == 0)) {
        el_id.classList.remove('alert-info');
        el_id.classList.add('alert-warning');
        el_id.classList.add('text-danger');
        invalid_alert('Remove "http://" or "https://" from ' + descr + "!");
        return false;
    } else {
        return true;
    };
};


function validate_ip(el_id, input) {
    // - Called from 'settings.js'
    // - Validates input for ip address

    var ipv4_6_re = /((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))/;

    if (!ipv4_6_re.test(input)) {
        el_id.classList.remove('alert-info');
        el_id.classList.add('alert-warning');
        el_id.classList.add('text-danger');
        invalid_alert('Improperly formatted IP address!');
        return false;
    } else {
        return true;
    }
};


function validate_email(el_id, input) {
    // - Called from 'settings.js'
    // - Validates input for email address

    var email_re = /\S+@\S+\.\S+/;

    if (!email_re.test(input)) {
        el_id.classList.remove('alert-info');
        el_id.classList.add('alert-warning');
        el_id.classList.add('text-danger');
        invalid_alert('Email is not properly formatted!');
        return false;
    } else {
        return true;
    };
};


function validate_phone(el_id, input) {
    // - Called from 'settings.js'
    // - Validates input for phone number

    var phone_na_raw_re = /^\d{10}/;
    var phone_na_format_re = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    var phone_plus_re = /^\+\d+/;
    var phone_intl_raw_re = /^\+\d{10}$/;
    var phone_intl_format_re = /^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{4})$/;

    if (phone_plus_re.test(input)) {
        if (!phone_intl_raw_re.test(input)) {
            if (!phone_intl_format_re.test(input)) {
                el_id.classList.remove('alert-info');
                el_id.classList.add('alert-warning');
                el_id.classList.add('text-danger');
                invalid_alert('Improperly formatted international number!');
                return false;
            } else {
                return true;
            };
        } else {
            return true;
        };

    } else {
        if (!phone_na_raw_re.test(input)) {
            if (!phone_na_format_re.test(input)) {
                el_id.classList.remove('alert-info');
                el_id.classList.add('alert-warning');
                el_id.classList.add('text-danger');
                invalid_alert('Improperly formatted north american number!');
                return false;
            } else {
                return true;
            };
        } else {
            return true;
        };
    };
};


// This section focuses on updating element and control values

function update_titles(data) {
    // - Called from 'setup.js'
    // - Called from 'settings.js'
    // - Updates 'index.html/#index_title' and 'navbar.html/#navbar_title'


    // Set 'index_title' value
    // Set 'navbar_title' value
    index_title.innerHTML = 'Janus ESS ' + data.name + ' (' + data.version + ')';
    navbar_title.innerHTML = '<b>Janus ESS ' + data.name + '</b>';
};


function update_settings_core(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_core' controls


    // Set 'id_fm_txt_settings_core_*' values
    txt_settings_core_sysname.value = data.name;
    txt_settings_core_customerid.value = data.customer;
    txt_settings_core_swver.value = data.version;
    txt_settings_core_iface.value = data.interface;
    txt_settings_core_mmap.value = data.map_version;
};


function update_settings_dataunits(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_dataunits' controls


    // Remove 'active' class from 'lbl_settings_dataunits_temp' elements
    // Add 'active' class to 'lbl_settings_dataunits_temp#'
    // Set property 'checked' on 'rad_settings_dataunits_temp#'
    remove_class(els_lbl_settings_dataunits_temp, 'active');
    ids_lbl_settings_dataunits_temp[data.temperature].classList.add('active');
    ids_rad_settings_dataunits_temp[data.temperature].checked = true;
    add_class(els_lbl_settings_dataunits_temp, 'alert-info');
    ids_lbl_settings_dataunits_temp[data.temperature].classList.remove('alert-info');
    remove_class(els_lbl_settings_dataunits_temp, 'btn_primary');
    ids_lbl_settings_dataunits_temp[data.temperature].classList.add('btn-primary');

    // Remove 'active' class from 'lbl_settings_dataunits_press' elements
    // Add 'active' class to 'lbl_settings_dataunits_press#'
    // Set property 'checked' on rad_settings_dataunits_press#'
    remove_class(els_lbl_settings_dataunits_press, 'active');
    ids_lbl_settings_dataunits_press[data.pressure].classList.add('active');
    ids_rad_settings_dataunits_press[data.pressure].checked = true;
    add_class(els_lbl_settings_dataunits_press, 'alert-info');
    ids_lbl_settings_dataunits_press[data.pressure].classList.remove('alert-info');
    remove_class(els_lbl_settings_dataunits_press, 'btn_primary');
    ids_lbl_settings_dataunits_press[data.pressure].classList.add('btn-primary');
};


function update_settings_log(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_log' controls


    // Remove 'active' class from 'cls_fm_lbl_settings_log_activity' elements
    // Add 'active' class to 'lbl_settings_log#_activity'
    // Set property 'checked' on 'rad_settings_log#_activity'
    remove_class(els_lbl_settings_log_activity, 'active');
    ids_lbl_settings_log_activity[data.activity].classList.add('active');
    ids_rad_settings_log_activity[data.activity].checked = true;
    add_class(els_lbl_settings_log_activity, 'alert-info');
    ids_lbl_settings_log_activity[data.activity].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_activity, 'btn_primary');
    ids_lbl_settings_log_activity[data.activity].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_janusess' elements
    // Add 'active' class to 'lbl_settings_log#_janusess'
    // Set property 'checked' on 'rad_settings_log#_janusess'
    remove_class(els_lbl_settings_log_janusess, 'active');
    ids_lbl_settings_log_janusess[data.janusess].classList.add('active');
    ids_rad_settings_log_janusess[data.janusess].checked = true;
    add_class(els_lbl_settings_log_janusess, 'alert-info');
    ids_lbl_settings_log_janusess[data.janusess].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_janusess, 'btn_primary');
    ids_lbl_settings_log_janusess[data.janusess].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_command' elements
    // Add 'active' class to 'lbl_settings_log#_command'
    // Set property 'checked' on 'rad_settings_log#_command'
    remove_class(els_lbl_settings_log_command, 'active');
    ids_lbl_settings_log_command[data.command].classList.add('active');
    ids_rad_settings_log_command[data.command].checked = true;
    add_class(els_lbl_settings_log_command, 'alert-info');
    ids_lbl_settings_log_command[data.command].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_command, 'btn_primary');
    ids_lbl_settings_log_command[data.command].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_conversion' elements
    // Add 'active' class to 'lbl_settings_log#_conversion'
    // Set property 'checked' on 'rad_settings_log#_conversion'
    remove_class(els_lbl_settings_log_conversion, 'active');
    ids_lbl_settings_log_conversion[data.conversion].classList.add('active');
    ids_rad_settings_log_conversion[data.conversion].checked = true;
    add_class(els_lbl_settings_log_conversion, 'alert-info');
    ids_lbl_settings_log_conversion[data.conversion].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_conversion, 'btn_primary');
    ids_lbl_settings_log_conversion[data.conversion].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_heartbeat' elements
    // Add 'active' class to 'lbl_settings_log#_heartbeat'
    // Set property 'checked' on 'rad_settings_log#_heartbeat'
    remove_class(els_lbl_settings_log_heartbeat, 'active');
    ids_lbl_settings_log_heartbeat[data.heartbeat].classList.add('active');
    ids_rad_settings_log_heartbeat[data.heartbeat].checked = true;
    add_class(els_lbl_settings_log_heartbeat, 'alert-info');
    ids_lbl_settings_log_heartbeat[data.heartbeat].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_heartbeat, 'btn_primary');
    ids_lbl_settings_log_heartbeat[data.heartbeat].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_interface' elements
    // Add 'active' class to 'lbl_settings_log#_interface'
    // Set property 'checked' on 'rad_settings_log#_interface'
    remove_class(els_lbl_settings_log_interface, 'active');
    ids_lbl_settings_log_interface[data.interface].classList.add('active');
    ids_rad_settings_log_interface[data.interface].checked = true;
    add_class(els_lbl_settings_log_interface, 'alert-info');
    ids_lbl_settings_log_interface[data.interface].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_interface, 'btn_primary');
    ids_lbl_settings_log_interface[data.interface].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_polling' elements
    // Add 'active' class to 'lbl_settings_log#_polling'
    // Set property 'checked' on 'rad_settings_log#_polling'
    remove_class(els_lbl_settings_log_polling, 'active');
    ids_lbl_settings_log_polling[data.polling].classList.add('active');
    ids_rad_settings_log_polling[data.polling].checked = true;
    add_class(els_lbl_settings_log_polling, 'alert-info');
    ids_lbl_settings_log_polling[data.polling].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_polling, 'btn_primary');
    ids_lbl_settings_log_polling[data.polling].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_server' elements
    // Add 'active' class to 'lbl_settings_log#_server'
    // Set property 'checked' on 'rad_settings_log#_server'
    remove_class(els_lbl_settings_log_server, 'active');
    ids_lbl_settings_log_server[data.server].classList.add('active');
    ids_rad_settings_log_server[data.server].checked = true;
    add_class(els_lbl_settings_log_server, 'alert-info');
    ids_lbl_settings_log_server[data.server].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_server, 'btn_primary');
    ids_lbl_settings_log_server[data.server].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_setup' elements
    // Add 'active' class to 'lbl_settings_log#_setup'
    // Set property 'checked' on 'rad_settings_log#_setup'
    remove_class(els_lbl_settings_log_setup, 'active');
    ids_lbl_settings_log_setup[data.setup].classList.add('active');
    ids_rad_settings_log_setup[data.setup].checked = true;
    add_class(els_lbl_settings_log_setup, 'alert-info');
    ids_lbl_settings_log_setup[data.setup].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_setup, 'btn_primary');
    ids_lbl_settings_log_setup[data.setup].classList.add('btn-primary');

    // Remove 'active' class from 'cls_fm_lbl_settings_log_tasks' elements
    // Add 'active' class to 'lbl_settings_log#_tasks'
    // Set property 'checked' on 'rad_settings_log#_tasks'
    remove_class(els_lbl_settings_log_tasks, 'active');
    ids_lbl_settings_log_tasks[data.tasks].classList.add('active');
    ids_rad_settings_log_tasks[data.tasks].checked = true;
    add_class(els_lbl_settings_log_tasks, 'alert-info');
    ids_lbl_settings_log_tasks[data.tasks].classList.remove('alert-info');
    remove_class(els_lbl_settings_log_tasks, 'btn_primary');
    ids_lbl_settings_log_tasks[data.tasks].classList.add('btn-primary');
};


function update_settings_compact(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_compact' controls


    // Set 'txt_settings_compact_*' values
    txt_settings_compact_firsttime.value = data.dbcompact_firsttime;
    nbr_settings_compact_interval.value = data.dbcompact_interval;

    // Clear any previous data invalidation indicators if data is valid
    txt_settings_compact_firsttime.classList.remove('alert-warning');
    txt_settings_compact_firsttime.classList.remove('text-danger');
    txt_settings_compact_firsttime.classList.add('alert-info');
    nbr_settings_compact_interval.classList.remove('alert-warning');
    nbr_settings_compact_interval.classList.remove('text-danger');
    nbr_settings_compact_interval.classList.add('alert-info');
};


function update_settings_update(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_update' controls


    // Set 'txt_settings_update_*' values
    txt_settings_update_firsttime.value = data.updateemail_firsttime;
    nbr_settings_update_interval.value = data.updateemail_interval;

    // Clear any previous data invalidation indicators if data is valid
    txt_settings_update_firsttime.classList.remove('alert-warning');
    txt_settings_update_firsttime.classList.remove('text-danger');
    txt_settings_update_firsttime.classList.add('alert-info');
    nbr_settings_update_interval.classList.remove('alert-warning');
    nbr_settings_update_interval.classList.remove('text-danger');
    nbr_settings_update_interval.classList.add('alert-info');
};


function update_settings_cloud(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_cloud' controls


    // Set 'txt_settings_cloud_url' value
    txt_settings_cloud_url.value = data.url;

    // Clear any previous data invalidation indicators if data is valid
    txt_settings_cloud_url.classList.remove('alert-warning');
    txt_settings_cloud_url.classList.remove('text-danger');

    // Set property 'checked' on 'chk_settings_cloud_en'
    // Toggle 'active' class on 'lbl_settings_cloud_en'
    chk_settings_cloud_en.checked = data.enable;
    if (data.enable == true) {
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


function update_settings_network(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_network' controls


    // Set 'txt_settings_network_*' values
    txt_settings_network_url.value = data.url_server;
    nbr_settings_network_intgood.value = data.interval_good;
    nbr_settings_network_intbad.value = data.interval_bad;
    nbr_settings_network_timeout.value = data.url_timeout;

    // Clear any previous data invalidation indicators if data is valid
    txt_settings_network_url.classList.add('alert-info');
    txt_settings_network_url.classList.remove('alert-warning');
    txt_settings_network_url.classList.remove('text-danger');
    nbr_settings_network_intgood.classList.add('alert-info');
    nbr_settings_network_intgood.classList.remove('alert-warning');
    nbr_settings_network_intgood.classList.remove('text-danger');
    nbr_settings_network_intbad.classList.add('alert-info');
    nbr_settings_network_intbad.classList.remove('alert-warning');
    nbr_settings_network_intbad.classList.remove('text-danger');
    nbr_settings_network_timeout.classList.add('alert-info');
    nbr_settings_network_timeout.classList.remove('alert-warning');
    nbr_settings_network_timeout.classList.remove('text-danger');
};


function update_settings_email(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_email' controls


    // Clear any previous data invalidation indicators if data is valid
    remove_class(els_settings_smtp, 'alert-warning');
    remove_class(els_settings_smtp, 'text-danger');

    // Set property 'checked' on 'chk_settings_smtp_en'
    // Toggle value on 'btn_settings_smtp_en'
    chk_settings_smtp_en.checked = data.smtp_enable;
    if (data.smtp_enable == true) {
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

    // Set 'txt_settings_email_*' values
    txt_settings_smtp_from.value = data.smtp_from;
    txt_settings_smtp_server.value = data.smtp_server;
    nbr_settings_smtp_port.value = data.smtp_port;
    nbr_settings_smtp_timeout.value = data.smtp_timeout;
    pwd_settings_smtp_pwd.value = data.smtp_password;
};


function update_settings_email_list(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_email' controls


    // Clear any previous data invalidation indicators if data is valid
    txt_settings_smtp_address.classList.add('alert-info');
    txt_settings_smtp_address.classList.remove('alert-warning');
    txt_settings_smtp_address.classList.remove('text-danger');

    // Clear 'txt_settings_smtp_address' value
    // Remove 'active' class from 'els_lbl_settings_smtp_list' controls
    // Add 'alert-info' class from 'els_lbl_settings_smtp_list' controls
    // Set property 'checked' on 'rad_settings_smtp0_list'
    // Toggle 'active' class on 'lbl_settings_smtp0_list'
    // Remove 'active' class from 'els_lbl_settings_smtp_choice' controls
    // Add 'alert-info' class from 'els_lbl_settings_smtp_choice' controls
    // Set property 'checked' on 'rad_settings_smtp0_choice'
    // Toggle 'active' class on 'lbl_settings_smtp0_choice'
    txt_settings_smtp_address.value = '';
    remove_class(els_lbl_settings_smtp_list, 'active');
    add_class(els_lbl_settings_smtp_list, 'alert-info');
    rad_settings_smtp0_list.checked = true;
    lbl_settings_smtp0_list.classList.add('active');
    lbl_settings_smtp0_list.classList.remove('alert-info');
    lbl_settings_smtp0_list.classList.add('btn-primary');
    remove_class(els_lbl_settings_smtp_choice, 'active');
    add_class(els_lbl_settings_smtp_choice, 'alert-info');
    rad_settings_smtp0_choice.checked = true;
    lbl_settings_smtp0_choice.classList.add('active');
    lbl_settings_smtp0_choice.classList.remove('alert-info');
    lbl_settings_smtp0_choice.classList.add('btn-primary');

    // Set 'btn_settings_smtp_list' value
    btn_settings_smtp_list.value = 'Modify Status Email List'

    // Remove child elements from 'tbody_settings_smtp_status'
    // Build table rows for SMS mobile numbers in 'tbody_settings_smtp_status'
    remove_elements(tbody_settings_smtp_status);
    for (var index in data.smtp_list_status) {
        var tbody_tr = document.createElement("tr");
        tbody_tr.id = 'smtp_list_status_' + index;
        var tbody_tr_td = document.createElement("td");
        tbody_tr_td.classList.add("col-sm-12");
        tbody_tr_td.classList.add("col-md-12");
        tbody_tr_td.classList.add("text-center");
        tbody_tr_td.classList.add('table-info');
        tbody_tr_td.innerHTML = '<small>' + data.smtp_list_status[index] + '</small>';
        tbody_tr.appendChild(tbody_tr_td);
        tbody_settings_smtp_status.appendChild(tbody_tr);
    };

    // Remove child elements from 'tbody_settings_smtp_alert'
    // Build table rows for SMS mobile numbers in 'tbody_settings_smtp_alert'
    remove_elements(tbody_settings_smtp_alert);
    for (var index in data.smtp_list_alert) {
        var tbody_tr = document.createElement("tr");
        tbody_tr.id = 'smtp_list_alert_' + index;
        var tbody_tr_td = document.createElement("td");
        tbody_tr_td.classList.add("col-sm-12");
        tbody_tr_td.classList.add("col-md-12");
        tbody_tr_td.classList.add("text-center");
        tbody_tr_td.classList.add('table-info');
        tbody_tr_td.innerHTML = '<small>' + data.smtp_list_alert[index] + '</small>';
        tbody_tr.appendChild(tbody_tr_td);
        tbody_settings_smtp_alert.appendChild(tbody_tr);
    };

    // Remove child elements from 'tbody_settings_smtp_error'
    // Build table rows for SMS mobile numbers in 'tbody_settings_smtp_error'
    remove_elements(tbody_settings_smtp_error);
    for (var index in data.smtp_list_error) {
        var tbody_tr = document.createElement("tr");
        tbody_tr.id = 'smtp_list_error_' + index;
        var tbody_tr_td = document.createElement("td");
        tbody_tr_td.classList.add("col-sm-12");
        tbody_tr_td.classList.add("col-md-12");
        tbody_tr_td.classList.add("text-center");
        tbody_tr_td.classList.add('table-info');
        tbody_tr_td.innerHTML = '<small>' + data.smtp_list_error[index] + '</small>';
        tbody_tr.appendChild(tbody_tr_td);
        tbody_settings_smtp_error.appendChild(tbody_tr);
    };
};


function update_settings_sms(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_sms' controls


    // Set property 'checked' on 'chk_settings_sms_en'
    // Toggle value on 'btn_settings_sms_en'
    chk_settings_sms_en.checked = data.sms_enable;
    if (data.sms_enable == true) {
        btn_settings_sms_en.classList.remove('btn-danger');
        btn_settings_sms_en.classList.add('alert-danger');
        btn_settings_sms_en.value = 'SMS Enabled';
    } else {
        btn_settings_sms_en.classList.remove('alert-danger');
        btn_settings_sms_en.classList.add('btn-danger');
        btn_settings_sms_en.value = 'SMS Disabled';
    };
};


function update_settings_sms_list(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_sms' controls


    // Clear any previous data invalidation indicators if data is valid
    txt_settings_sms_mobile.classList.add('alert-info');
    txt_settings_sms_mobile.classList.remove('alert-warning');
    txt_settings_sms_mobile.classList.remove('text-danger');

    // Clear 'txt_settings_sms_mobile' value
    // Set 'btn_settings_sms_gateways' innerHTML
    // Remove 'active' class from 'btn_settings_sms_gateways'
    // Remove 'active' class from 'els_lbl_settings_sms_list' controls
    // Add 'alert-info' class from 'els_lbl_settings_sms_list' controls
    // Set property 'checked' on 'rad_settings_sms0_list'
    // Toggle 'active' class on 'lbl_settings_sms0_list'
    txt_settings_sms_mobile.value = '';
    btn_settings_sms_gateways.innerHTML = 'Select Carrier';
    if (btn_settings_sms_gateways.classList.contains('active')) {
        btn_settings_sms_gateways.classList.remove('active');
    };
    remove_class(els_lbl_settings_sms_list, 'active');
    add_class(els_lbl_settings_sms_list, 'alert-info');
    rad_settings_sms0_list.checked = true;
    lbl_settings_sms0_list.classList.add('active');
    lbl_settings_sms0_list.classList.remove('alert-info');
    lbl_settings_sms0_list.classList.add('btn-primary');

    // Set 'btn_settings_sms_list' value
    btn_settings_sms_list.value = 'Modify Status SMS List'

    // Remove child elements from 'dm_settings_sms_carriers'
    remove_elements(dm_settings_sms_carriers);

    // Build 'Delete Number' item for SMS carriers in 'dm_settings_sms_carriers'
    var carrier_delete = document.createElement("a");
    carrier_delete.id = "a_settings_sms_carrier_delete";
    carrier_delete.classList.add("dropdown-item");
    carrier_delete.classList.add("bg-danger");
    carrier_delete.classList.add("text-warning");
    carrier_delete.setAttribute(
        "onclick",
        "a_clk_dm_settings_sms_gateways_toggle('Delete Number', 'delete');"
    );
    carrier_delete.setAttribute("href", "javascript:void(0);");
    carrier_delete.innerHTML = "Delete Number"
    dm_settings_sms_carriers.appendChild(carrier_delete);

    // Build divider for SMS carriers in 'dm_settings_sms_carriers'
    var carrier_divide = document.createElement("div");
    carrier_divide.id = "settings_sms_carrier_divider";
    carrier_divide.classList.add("dropdown-divider");
    dm_settings_sms_carriers.appendChild(carrier_divide);

    // Build carrier items for SMS carriers in 'dm_settings_sms_carriers'
    var index = 0;
    for (var key in data.sms_carriers) {
        var carrier_a = document.createElement("a");
        carrier_a.id = 'a_settings_sms_carrier' + index;
        carrier_a.classList.add("dropdown-item");
        carrier_a.classList.add("bg-success");
        carrier_a.classList.add("text-warning");
        carrier_a.setAttribute(
            "onclick",
            "a_clk_dm_settings_sms_gateways_toggle('" + key + "', '" + data.sms_carriers[key] + "');"
        );
        carrier_a.setAttribute("href", "javascript:void(0);");
        carrier_a.innerHTML = key;
        dm_settings_sms_carriers.appendChild(carrier_a);
        index += 1;
    };

    // Remove child elements from 'tbody_settings_sms_status'
    // Build table rows for SMS mobile numbers in 'tbody_settings_sms_status'
    remove_elements(tbody_settings_sms_status);
    for (var index in data.sms_list_status) {
        var mobile = data.sms_list_status[index].split('@');
        var tbody_tr = document.createElement("tr");
        tbody_tr.id = 'sms_list_status_' + index;
        var tbody_tr_td = document.createElement("td");
        tbody_tr_td.classList.add("col-sm-12");
        tbody_tr_td.classList.add("col-md-12");
        tbody_tr_td.classList.add("text-center");
        tbody_tr_td.classList.add('table-info');
        tbody_tr_td.innerHTML = '<small>' + mobile[0] + '</small>';
        tbody_tr.appendChild(tbody_tr_td);
        tbody_settings_sms_status.appendChild(tbody_tr);
    };

    // Remove child elements from 'tbody_settings_sms_alert'
    // Build table rows for SMS mobile numbers in 'tbody_settings_sms_alert'
    remove_elements(tbody_settings_sms_alert);
    for (var index in data.sms_list_alert) {
        var mobile = data.sms_list_alert[index].split('@');
        var tbody_tr = document.createElement("tr");
        tbody_tr.id = 'sms_list_alert_' + index;
        var tbody_tr_td = document.createElement("td");
        tbody_tr_td.classList.add("col-sm-12");
        tbody_tr_td.classList.add("col-md-12");
        tbody_tr_td.classList.add("text-center");
        tbody_tr_td.classList.add('table-info');
        tbody_tr_td.innerHTML = '<small>' + mobile[0] + '</small>';
        tbody_tr.appendChild(tbody_tr_td);
        tbody_settings_sms_alert.appendChild(tbody_tr);
    };

    // Remove child elements from 'tbody_settings_sms_error'
    // Build table rows for SMS mobile numbers in 'tbody_settings_sms_error'
    remove_elements(tbody_settings_sms_error);
    for (var index in data.sms_list_error) {
        var mobile = data.sms_list_error[index].split('@');
        var tbody_tr = document.createElement("tr");
        tbody_tr.id = 'sms_list_error_' + index;
        var tbody_tr_td = document.createElement("td");
        tbody_tr_td.classList.add("col-sm-12");
        tbody_tr_td.classList.add("col-md-12");
        tbody_tr_td.classList.add("text-center");
        tbody_tr_td.classList.add('table-info');
        tbody_tr_td.innerHTML = '<small>' + mobile[0] + '</small>';
        tbody_tr.appendChild(tbody_tr_td);
        tbody_settings_sms_error.appendChild(tbody_tr);
    };
};


function update_settings_snmp(data) {
    // - Called from 'settings.js'
    // - Called from 'sidebar_settings.js'
    // - Updates 'settings.html/#settings_snmp' controls


    // Clear any previous data invalidation indicators if data is valid
    txt_settings_snmp_server.classList.remove('alert-warning');
    txt_settings_snmp_server.classList.remove('text-danger');
    nbr_settings_snmp_port.classList.remove('alert-warning');
    nbr_settings_snmp_port.classList.remove('text-danger');

    // Set property 'checked' on 'chk_settings_snmp_agent_en'
    // Toggle 'active' class on 'lbl_settings_snmp_agent_en'
    chk_settings_snmp_agent_en.checked = data.agent_enable;
    if (data.agent_enable == true) {
        btn_settings_snmp_agent_en.classList.remove('btn-danger');
        btn_settings_snmp_agent_en.classList.add('alert-danger');
        btn_settings_snmp_agent_en.value = 'SNMP Agent Enabled';
    } else {
        btn_settings_snmp_agent_en.classList.remove('alert-danger');
        btn_settings_snmp_agent_en.classList.add('btn-danger');
        btn_settings_snmp_agent_en.value = 'SNMP Agent Disabled';
    };

    // Set property 'checked' on 'chk_settings_snmp_notify_en'
    // Toggle 'active' class on 'lbl_settings_snmp_notify_en'
    chk_settings_snmp_notify_en.checked = data.notify_enable;
    if (data.notify_enable == true) {
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

    // Set 'txt_settings_snmp_*' values
    txt_settings_snmp_server.value = data.server;
    nbr_settings_snmp_port.value = data.port;
    txt_settings_snmp_comm.value = data.community;
};

