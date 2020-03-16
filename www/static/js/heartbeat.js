// Author: Larry A. Hartman
// Company: Janus Research Group


// Initialize global websocket variable, this will be set to function object later
var ws;

heartbeat_activity = function (data) {
    // - Called from 'heartbeat.js/function ws()'
    // - Builds presentable message packet
    // - Adds heartbeat activity statement to scrolling list on 'status.html'


    // Build HTML message packet
    var line_p = document.createElement("p");
    if (data.search('DEBUG') == 20) {
        line_p.classList.add('text-success');
        line_p.classList.add('bg-ight');
    } else if (data.search('INFO') == 20) {
        line_p.classList.add('text-primary');
        line_p.classList.add('bg-light');
    } else if (data.search('WARNING') == 20) {
        line_p.classList.add('text-success');
        line_p.classList.add('bg-warning');
    } else if (data.search('ERROR') == 20) {
        line_p.classList.add('text-primary');
        line_p.classList.add('bg-warning');
    } else if (data.search('CRITICAL') == 20) {
        line_p.classList.add('text-warning');
        line_p.classList.add('bg-danger');
    } else {
        line_p.classList.add('text-black');
        line_p.classList.add('bg-white');
    };
    line_p.style.margin = '0.0px';
    line_p.style.padding = '0.0px';
    line_p.style.lineHeight = '1.1em';
    line_p.innerHTML = data;

    // Place activity statement ahead of others in list
    $("div#status_base_activity_receive").prepend(line_p);
    console.log(data);
};


function heartbeat_base(field) {
    // - Called from 'heartbeat.js/function ws()'
    // - Updates base unit process status on 'status.html'
    //
    // field[1] = process
    // field[2] = process status

    // Set status.html process status messages and styles
    if (field[1] != 'network') {
        ids_status_base[field[1]].innerHTML = status_messages[field[2]];
    } else {
        ids_status_base[field[1]].classList.remove('alert-info');
    };
    remove_status_classes(ids_status_base[field[1]]);
    add_status_classes(field[2], ids_status_base[field[1]]);
};

function heartbeat_network(field) {
    // - Called from 'heartbeat.js/function ws()'
    // - Updates network status on 'status.html'
    //
    // field[1] = check url
    // field[2] = check interval
    // field[3] = check dtg

    // Set network status message
    status_base_network.innerHTML = "Last network check with " + field[1] + " was " +
        "conducted at: " + field[3] + ".  Next check will " +
        "take place in " + field[2] + " minutes after last check.";
};

function heartbeat_lane(field) {
    // - Called from 'heartbeat.js/function ws()'
    // - Updates lane status on 'status.html' and 'setup.html'
    // - Toggles display visibility for 'poll/modules.html'
    // - Toggles control enable for 'setup/poll.html'
    //
    // field[1] = lane address
    // field[2] = lane status
    // field[3] = last module
    // field[4] = polling status
    // field[5] = last poll dtg
    // field[6] = setup id


    // Convert field values to numbers
    field[2] = parseInt(field[2], 10);
    field[3] = parseInt(field[3], 10);
    field[4] = parseInt(field[4], 10);

    // Set status message and styles on status.html and poll.html
    var lane_status = status_messages[field[2]];
    var lane_status_sym = status_symbols[field[2]];
    ids_status_base_lane_status[field[1]].innerHTML = lane_status;
    remove_status_classes(ids_status_base_lane_status[field[1]]);
    add_status_classes(field[2], ids_status_base_lane_status[field[1]]);
    ids_span_lane_status[field[1]].innerHTML = lane_status;
    ids_span_lane_status_sym[field[1]].innerHTML = lane_status_sym;
    remove_status_classes(ids_btn_lane_status[field[1]]);
    add_status_classes(field[2], ids_btn_lane_status[field[1]]);

    // Set number of modules on sidebar
    ids_span_sidebar_lanes_mods[field[1]].innerHTML = field[3];

    // Toggle visibility for poll.html and modules.html elements
    if (field[2] < stat_lvl['crit']) {
        ids_lane_modules[field[1]].classList.remove('d-none');
        ids_lane_modules[field[1]].classList.add('d-block');
    } else {
        ids_lane_modules[field[1]].classList.remove('d-block');
        ids_lane_modules[field[1]].classList.add('d-none');
    };

    // Check for already built carousel, get its start and end points
    // Requires change of state marker as module numbers are incremented
    module_last = 0;
    lane_mod_prev = null;
    for (module = 1; module <= 126; module++) {
        lane_mod_id = 'lane' + field[1] + '_module' + module;
        lane_mod = document.getElementById(lane_mod_id);
        if ((lane_mod == null) && (lane_mod_prev != null)) {
            module_last = module - 1;
        };
        lane_mod_prev = lane_mod;
    };

    // Setup module carousel if not setup or changes detected
    if (module_last != field[3]) {
        //remove_elements(ids_lane_modules_cards[field[1]]);
        if (field[2] <= stat_lvl['crit']) {
            lane_module_card_deck(field[1], field[6], field[3]);
        };
    };

    // Set status.html polling status messages and styles
    remove_status_classes(ids_status_base_lane_polling[field[1]]);
    add_status_classes(field[4], ids_status_base_lane_polling[field[1]]);

    if (field[4] == stat_lvl['op']) {
        var poll_status = 'Last poll was ' + field[5] + '.';
    } else {
        var poll_status = status_messages[field[4]];
    };
    ids_status_base_lane_polling[field[1]].innerHTML = poll_status;

    // Enable/disable poll.html start polling controls
    if (field[2] < stat_lvl['crit']) {
        if ((field[4] < stat_lvl['not_cfg'] ) || (field[4] > stat_lvl['undeter'])) {
            ids_btn_lane_poll_start[field[1]].disabled = true;
            ids_btn_lane_poll_start[field[1]].classList.remove('btn-info');
            ids_btn_lane_poll_start[field[1]].classList.add('btn-secondary');
            ids_btn_lane_poll_clear[field[1]].disabled = true;
            ids_btn_lane_poll_clear[field[1]].classList.remove('btn-info');
            ids_btn_lane_poll_clear[field[1]].classList.add('btn-secondary');
        } else if ((field[4] > 3) && (field[4] <= 5)) {
            ids_btn_lane_poll_start[field[1]].disabled = false;
            ids_btn_lane_poll_start[field[1]].classList.remove('btn-secondary');
            ids_btn_lane_poll_start[field[1]].classList.add('btn-info');
            ids_btn_lane_poll_clear[field[1]].disabled = false;
            ids_btn_lane_poll_clear[field[1]].classList.remove('btn-secondary');
            ids_btn_lane_poll_clear[field[1]].classList.add('btn-info');
        };

        // Enable/disable poll.html stop polling controls, call function to clear sensors
        if (field[4] < stat_lvl['crit']) {
            ids_btn_lane_poll_stop[field[1]].disabled = false;
            ids_btn_lane_poll_stop[field[1]].classList.remove('btn-secondary');
            ids_btn_lane_poll_stop[field[1]].classList.add('btn-info');
            ids_btn_lane_reset[field[1]].disabled = true;
            ids_btn_lane_reset[field[1]].classList.remove('btn-danger');
            ids_btn_lane_reset[field[1]].classList.add('btn-secondary');
        } else {
            ids_btn_lane_poll_stop[field[1]].disabled = true;
            ids_btn_lane_poll_stop[field[1]].classList.remove('btn-info');
            ids_btn_lane_poll_stop[field[1]].classList.add('btn-secondary');
            ids_btn_lane_reset[field[1]].disabled = false;
            ids_btn_lane_reset[field[1]].classList.remove('btn-secondary');
            ids_btn_lane_reset[field[1]].classList.add('btn-danger');
        };
    } else {
        ids_btn_lane_poll_start[field[1]].disabled = true;
        ids_btn_lane_poll_start[field[1]].classList.remove('btn-info');
        ids_btn_lane_poll_start[field[1]].classList.add('btn-secondary');
        ids_btn_lane_poll_clear[field[1]].disabled = false;
        ids_btn_lane_poll_clear[field[1]].classList.remove('btn-secondary');
        ids_btn_lane_poll_clear[field[1]].classList.add('btn-info');
        ids_btn_lane_poll_stop[field[1]].disabled = true;
        ids_btn_lane_poll_stop[field[1]].classList.remove('btn-info');
        ids_btn_lane_poll_stop[field[1]].classList.add('btn-secondary');
        ids_btn_lane_reset[field[1]].disabled = false;
        ids_btn_lane_reset[field[1]].classList.remove('btn-secondary');
        ids_btn_lane_reset[field[1]].classList.add('btn-danger');
    };
};

function heartbeat_module(field) {
    // - Called from 'heartbeat.js/function ws()'
    // - Updates 'modconfig.html' module status
    //
    // field[1] = lane address
    // field[2] = module address
    // field[3] = module status

    // Get modules.html elements
    var lane_mod_body_stat_id = 'lane' + field[1] + '_module' + field[2] + '_status';
    var lane_mod_body_stat = document.getElementById(lane_mod_body_stat_id);
    var lane_mod_status_id = 'span_lane' + field[1] + '_module' + field[2] + '_status';
    var lane_mod_status = document.getElementById(lane_mod_status_id);
    var lane_mod_sym_id = 'span_lane' + field[1] + '_module' + field[2] + '_sym';
    var lane_mod_sym = document.getElementById(lane_mod_sym_id);
    var lane_mod_sensor_id = 'th_lane' + field[1] + '_module' + field[2] + '_sensor';
    var lane_mod_sensor = document.getElementById(lane_mod_sensor_id);

    // Set module status messages and styles, if element is built in document
    if (lane_mod_status != null) {
        remove_status_classes(lane_mod_body_stat)
        lane_mod_body_stat.classList.add(status_bg_class[field[3]]);
        lane_mod_body_stat.classList.add(status_text_class[field[3]]);

        lane_mod_status.innerHTML = '<b>' + status_messages[field[3]] + '</b>';
        lane_mod_sym.innerHTML = status_symbols[field[3]];
    };

    field[3] = parseInt(field[3], 10);
    if (field[3] == stat_lvl['s_evt']) {
        var module_data_id = 'lane' + field[1] + '_module' + field[2] + '_data';
        var module_data = document.getElementById(module_data_id);

        if (module_data.classList.contains('d-none')) {
            lane_mod_sensor.classList.remove('bg-dark');
            lane_mod_sensor.classList.add('bg-magenta');
            lane_mod_sensor.innerHTML = '<b>Check Sensors!</b>';

            var lane_mod_table_thead_tr_th_span = document.createElement('span');
            var lane_mod_table_thead_tr_th_span_id = 'lane' + field[1] + '_module' + field[2] + '_datatoggle';
            lane_mod_table_thead_tr_th_span.id = lane_mod_table_thead_tr_th_span_id;
            lane_mod_table_thead_tr_th_span.classList.add('pl-2');
            lane_mod_table_thead_tr_th_span.innerHTML = '<i class="fas fa-angle-down"></i>';
            var fn_mod_data = 'span_clk_module_data(' + field[1] + ', ' + field[2] + ');'
            lane_mod_table_thead_tr_th_span.setAttribute('onclick', fn_mod_data);
            lane_mod_sensor.appendChild(lane_mod_table_thead_tr_th_span);
        };
    };

    // Enable/disable individual polling button dependent upon module status
    var lane_mod_btn_modpoll_id = 'a_lane' + field[1] + '_module' + field[2] + '_poll';
    var lane_mod_btn_modpoll = document.getElementById(lane_mod_btn_modpoll_id)

    // Set module on-demand poll styles, if element is built in document
    if (lane_mod_btn_modpoll != null) {
        if (field[3] <= stat_lvl['op_err']) {
            lane_mod_btn_modpoll.disabled = false;
            lane_mod_btn_modpoll.classList.remove('alert-secondary');
            lane_mod_btn_modpoll.classList.add('btn-info');
        } else if (field[3] >= stat_lvl['crit']) {
            lane_mod_btn_modpoll.disabled = true;
            lane_mod_btn_modpoll.classList.remove('btn-info');
            lane_mod_btn_modpoll.classList.add('alert-secondary');
        };
    };
};

function heartbeat_poll(field) {
    // - Called from 'heartbeat.js/function ws()'
    // - Updates 'modconfig.html' sensor statuses
    //
    // field[1] = lane address
    // field[2] = module address
    // field[3] = sensor address
    // field[4] = module location
    // field[5] = sensor type
    // field[6] = sensor value
    // field[7] = sensor unit
    // field[8] = sensor value dtg
    // field[9] = alert type
    // field[10] = trigger threshold

    // Get modules.html sensor table elements
    var lane_modval_id = 'lane' + field[1] + '_module' + field[2] + '_sensor' + field[3] + '_value';
    var lane_modval = document.getElementById(lane_modval_id);
    var lane_trigger_id = 'lane' + field[1] + '_module' + field[2] + '_sensor' + field[3] + '_trigger';
    var lane_trigger = document.getElementById(lane_trigger_id);
    var lane_moddtg_id = 'lane' + field[1] + '_module' + field[2] + '_dtg';
    var lane_moddtg = document.getElementById(lane_moddtg_id);

    // Set sensor value and dtg element messages
    if (lane_modval != null) {
        lane_modval.innerHTML = '<small><b>' + field[6] + ' ' + field[7] + '</b></small>';
        lane_modval.classList.remove('table-info');
    };
    if (lane_moddtg != null) {
        lane_moddtg.innerHTML = '<i>Last Update: ' + field[8] + '</i>';
        lane_moddtg.classList.remove('table-info');
    };

    // Set sensor trigger messages and styles
    lane_trigger.className = '';
    lane_trigger.classList.add('col-4');
    if (field[9] == 'low') {
        if (lane_trigger != null) {
            lane_trigger.classList.add('bg-primary');
            lane_trigger.classList.add('text-white');
            lane_trigger.innerHTML = '<small><b>-' + (parseFloat(field[10]) - parseFloat(field[6])).toFixed(1) +
                '</b></small>';
        };
        message = 'Lane ' + field[1] + ' module ' + field[2] + ' ' + field[5] + ' sensor ' +
            'at location ' + field [4] + ' recorded a low value: ' + field[6] + ' ' + field[7] + ', ' +
            (parseFloat(field[10]) - parseFloat(field[6])).toFixed(1) + ' ' + field[7] + ' below set trigger.';
//        sensor_low_alert(message);

    } else if (field[9] == 'high') {
        if (lane_trigger != null) {
            lane_trigger.classList.add('bg-danger');
            lane_trigger.classList.add('text-warning');
            lane_trigger.innerHTML = '<small><b>+' + (parseFloat(field[6]) - parseFloat(field[10])).toFixed(1) +
                '</b></small>';
        };
        message = 'Lane ' + field[1] + ' module ' + field[2] + ' ' + field[5] + ' sensor ' +
            'at location ' + field [4] + ' recorded a high value: ' + field[6] + ' ' + field[7] + ', ' +
            (parseFloat(field[6]) - parseFloat(field[10])).toFixed(1) + ' ' + field[7] + ' above set trigger.';
//        sensor_high_alert(message);

    } else {
        if (lane_trigger != null) {
            lane_trigger.classList.add('bg-success');
            lane_trigger.classList.add('text-warning');
            lane_trigger.innerHTML = '<small><b>Normal</b></small>';
        };
    };
};

$(document).ready(function () {

    // Create websocket instance
    ws = new WebSocket("wss://" + window.location.host + '/websocket/');

    // Handle incoming websocket message callback
    // field[0] = heartbeat message
    ws.onmessage = function (evt) {
        var field = evt.data.split("/");
        switch(field[0]) {
            case 'activity':
                heartbeat_activity(field[1]);
                break;
            case 'base':
                heartbeat_base(field);
                break;
            case 'network':
                heartbeat_network(field);
                break;
            case 'lane':
                heartbeat_lane(field);
                break;
            case 'module':
                heartbeat_module(field);
                break;
            case 'poll':
                heartbeat_poll(field);
                break;
        };
    };

    // Open Websocket callback
    ws.onopen = function (evt) {
        heartbeat_activity("*** Websocket connection opened on: " + window.location.host + " ***");
    };

    window.onbeforeunload = function() {
        ws.onclose = function () {}; // disable onclose handler first
        ws.close();
    };
});