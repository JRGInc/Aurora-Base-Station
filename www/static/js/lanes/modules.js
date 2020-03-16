// Author: Larry A. Hartman
// Company: Janus Research Group


function lane_module_card_deck(lane, lane_setup_id, last_module) {
    // - Called from 'sidebar_lanes.js/a_clk_lane_sidebar_toggle()'
    // - Builds and attaches 'modules.html/#ol_lane*_indicator' elements
    // - Builds and attaches 'modules.html/#lane*_inner' elements
    // - Gets values for and assigns classes to 'modules.html#lane*_module*_status' element

    // AJAX call to get module status value from server and assign classes to status element
    $.ajax({
        url: '/',
        dataType: 'json',
        data: {
            dataset: 'modstatus',
            lane_address: lane,
        },
        type: "GET",
        success: function ( mod_data ) {

            remove_elements(ids_lane_modules_cards[lane]);

            for (dict = 0; dict < mod_data.length; dict++) {

                // Set value of hidden control field
                var module = mod_data[dict];
                if (module['value']['setup_id'].toString() == lane_setup_id) {

                    var lane_mod = document.createElement("div");
                    lane_mod.id = 'lane' + lane + '_module' + module['key'];
                    lane_mod.classList.add('mx-2');
                    lane_mod.classList.add('col-12');
                    lane_mod.classList.add('col-md-5');
                    lane_mod.classList.add('col-xl-3');
                    lane_mod.classList.add('card');
                    lane_mod.classList.add('text-center');
                    lane_mod.classList.add('px-0');
                    lane_mod.classList.add('bg-tope');

                    var lane_mod_uid = document.createElement("input");
                    lane_mod_uid.id = 'lane' + lane + '_module' + module['key'] + '_mod_uid';
                    lane_mod_uid.setAttribute('type', 'hidden');
                    lane_mod_uid.value = module['id'];
                    lane_mod.appendChild(lane_mod_uid);

                    var lane_mod_hdr = document.createElement("nav");
                    lane_mod_hdr.classList.add('card-header');
                    lane_mod_hdr.classList.add('navbar');
                    lane_mod_hdr.classList.add('navbar-expand-sm');
                    lane_mod_hdr.classList.add('navbar-dark');
                    lane_mod_hdr.classList.add('bg-dark');

                    var lane_mod_hdr_nav = document.createElement('div');
                    lane_mod_hdr_nav.classList.add('dropdown');
                    lane_mod_hdr_nav.classList.add('show');

                    var lane_mod_hdr_nav_act = document.createElement("a");
                    lane_mod_hdr_nav_act.id = 'lane' + lane + '_module' + module['key'] + '_dropdown'
                    lane_mod_hdr_nav_act.classList.add("btn");
                    lane_mod_hdr_nav_act.classList.add("btn-info");
                    lane_mod_hdr_nav_act.classList.add("dropdown-toggle");
                    lane_mod_hdr_nav_act.classList.add("text-white");
                    lane_mod_hdr_nav_act.setAttribute('data-toggle', 'dropdown');
                    lane_mod_hdr_nav_act.setAttribute('aria-haspopup', 'true');
                    lane_mod_hdr_nav_act.setAttribute('aria-expanded', 'false');
                    lane_mod_hdr_nav_act.setAttribute('role', 'button');
                    lane_mod_hdr_nav_act.innerHTML = '<i class="fas fa-bullhorn"></i>';

                    var lane_mod_hdr_nav_act_span = document.createElement('span');
                    lane_mod_hdr_nav_act_span.classList.add('pl-2');
                    lane_mod_hdr_nav_act_span.innerHTML = 'Actions';
                    lane_mod_hdr_nav_act.appendChild(lane_mod_hdr_nav_act_span);
                    lane_mod_hdr_nav.appendChild(lane_mod_hdr_nav_act);

                    var lane_mod_hdr_nav_drop = document.createElement('div');
                    lane_mod_hdr_nav_drop.classList.add('dropdown-menu');
                    lane_mod_hdr_nav_drop.classList.add('bg-tope');
                    lane_mod_hdr_nav_drop.setAttribute('aria-labelledby', lane_mod_hdr_nav_act.id);

                    var lane_mod_hdr_nav_drop_poll = document.createElement("a");
                    lane_mod_hdr_nav_drop_poll.id = 'a_lane' + lane + '_module' + module['key'] + '_poll';
                    lane_mod_hdr_nav_drop_poll.classList.add('dropdown-item');
                    lane_mod_hdr_nav_drop_poll.classList.add('btn');
                    lane_mod_hdr_nav_drop_poll.classList.add('mb-1');

                    if (module['value']['status'] <= stat_lvl['op_err']) {
                        lane_mod_hdr_nav_drop_poll.classList.remove('bg-secondary');
                        lane_mod_hdr_nav_drop_poll.classList.remove('text-dark');
                        lane_mod_hdr_nav_drop_poll.classList.add('bg-info');
                        lane_mod_hdr_nav_drop_poll.classList.add('text-white');
                        lane_mod_hdr_nav_drop_poll.disabled = false;
                    } else {
                        lane_mod_hdr_nav_drop_poll.classList.remove('bg-info');
                        lane_mod_hdr_nav_drop_poll.classList.remove('text-white');
                        lane_mod_hdr_nav_drop_poll.classList.add('bg-secondary');
                        lane_mod_hdr_nav_drop_poll.classList.add('text-dark');
                        lane_mod_hdr_nav_drop_poll.disabled = true;
                    };

                    var fn_mod_poll = 'btn_clk_module_poll(' + lane + ', ' + module['key'] + ');'
                    lane_mod_hdr_nav_drop_poll.setAttribute('onclick', fn_mod_poll);
                    lane_mod_hdr_nav_drop_poll.innerHTML = '<i class="fas fa-asterisk"></i>';

                    var lane_mod_hdr_nav_drop_poll_span = document.createElement('span');
                    lane_mod_hdr_nav_drop_poll_span.classList.add('ml-2');
                    lane_mod_hdr_nav_drop_poll_span.innerHTML = 'Poll';
                    lane_mod_hdr_nav_drop_poll.appendChild(lane_mod_hdr_nav_drop_poll_span);

                    lane_mod_hdr_nav_drop.appendChild(lane_mod_hdr_nav_drop_poll);

                    var lane_mod_hdr_nav_drop_locate = document.createElement("a");
                    lane_mod_hdr_nav_drop_locate.id = 'a_lane' + lane + '_module' + module['key'] + '_led_locate';
                    lane_mod_hdr_nav_drop_locate.classList.add('dropdown-item');
                    lane_mod_hdr_nav_drop_locate.classList.add('btn');
                    lane_mod_hdr_nav_drop_locate.classList.add('mb-1');

                    if (module['value']['status'] <= stat_lvl['op_err']) {
                        lane_mod_hdr_nav_drop_locate.classList.remove('bg-secondary');
                        lane_mod_hdr_nav_drop_locate.classList.remove('text-dark');
                        lane_mod_hdr_nav_drop_locate.classList.add('bg-info');
                        lane_mod_hdr_nav_drop_locate.classList.add('text-white');
                        lane_mod_hdr_nav_drop_locate.disabled = false;
                    } else {
                        lane_mod_hdr_nav_drop_locate.classList.remove('bg-info');
                        lane_mod_hdr_nav_drop_locate.classList.remove('text-white');
                        lane_mod_hdr_nav_drop_locate.classList.add('bg-secondary');
                        lane_mod_hdr_nav_drop_locate.classList.add('text-dark');
                        lane_mod_hdr_nav_drop_locate.disabled = true;
                    };

                    var fn_mod_locate = 'btn_clk_module_led("locate",' + lane + ', ' + module['key'] + ');'
                    lane_mod_hdr_nav_drop_locate.setAttribute('onclick', fn_mod_locate);
                    lane_mod_hdr_nav_drop_locate.innerHTML = '<i class="fas fa-lightbulb"></i>';

                    var lane_mod_hdr_nav_drop_locate_span = document.createElement('span');
                    lane_mod_hdr_nav_drop_locate_span.classList.add('ml-2');
                    lane_mod_hdr_nav_drop_locate_span.innerHTML = 'Locate';
                    lane_mod_hdr_nav_drop_locate.appendChild(lane_mod_hdr_nav_drop_locate_span);

                    lane_mod_hdr_nav_drop.appendChild(lane_mod_hdr_nav_drop_locate);

                    var lane_mod_hdr_nav_drop_heartbeat = document.createElement("a");
                    lane_mod_hdr_nav_drop_heartbeat.id = 'a_lane' + lane + '_module' + module['key'] + '_led_heartbeat';
                    lane_mod_hdr_nav_drop_heartbeat.classList.add('dropdown-item');
                    lane_mod_hdr_nav_drop_heartbeat.classList.add('btn');

                    if (module['value']['status'] <= stat_lvl['op_err']) {
                        lane_mod_hdr_nav_drop_heartbeat.classList.remove('bg-secondary');
                        lane_mod_hdr_nav_drop_heartbeat.classList.remove('text-dark');
                        lane_mod_hdr_nav_drop_heartbeat.classList.add('bg-info');
                        lane_mod_hdr_nav_drop_heartbeat.classList.add('text-white');
                        lane_mod_hdr_nav_drop_heartbeat.disabled = false;
                    } else {
                        lane_mod_hdr_nav_drop_heartbeat.classList.remove('bg-info');
                        lane_mod_hdr_nav_drop_heartbeat.classList.remove('text-white');
                        lane_mod_hdr_nav_drop_heartbeat.classList.add('bg-secondary');
                        lane_mod_hdr_nav_drop_heartbeat.classList.add('text-dark');
                        lane_mod_hdr_nav_drop_heartbeat.disabled = true;
                    };

                    var fn_mod_heartbeat = 'btn_clk_module_led("heartbeat",' + lane + ', ' + module['key'] + ');'
                    lane_mod_hdr_nav_drop_heartbeat.setAttribute('onclick', fn_mod_heartbeat);
                    lane_mod_hdr_nav_drop_heartbeat.innerHTML = '<i class="fas fa-heartbeat"></i>';

                    var lane_mod_hdr_nav_drop_heartbeat_span = document.createElement('span');
                    lane_mod_hdr_nav_drop_heartbeat_span.classList.add('ml-2');
                    lane_mod_hdr_nav_drop_heartbeat_span.innerHTML = 'Heartbeat';
                    lane_mod_hdr_nav_drop_heartbeat.appendChild(lane_mod_hdr_nav_drop_heartbeat_span);

                    lane_mod_hdr_nav_drop.appendChild(lane_mod_hdr_nav_drop_heartbeat);

                    lane_mod_hdr_nav.appendChild(lane_mod_hdr_nav_drop);
                    lane_mod_hdr.appendChild(lane_mod_hdr_nav);

                    var lane_mod_hdr_brand = document.createElement("div");
                    lane_mod_hdr_brand.classList.add('navbar-brand');
                    lane_mod_hdr_brand.classList.add('ml-1');
                    lane_mod_hdr_brand.classList.add('d-lg-none');
                    lane_mod_hdr_brand.innerHTML = '<small>' + module['value']['descr'] + '<small>';
                    lane_mod_hdr.appendChild(lane_mod_hdr_brand);

                    var lane_mod_hdr_brand = document.createElement("div");
                    lane_mod_hdr_brand.classList.add('navbar-brand');
                    lane_mod_hdr_brand.classList.add('ml-1');
                    lane_mod_hdr_brand.classList.add('d-none');
                    lane_mod_hdr_brand.classList.add('d-lg-inline');
                    lane_mod_hdr_brand.innerHTML = module['value']['descr'];
                    lane_mod_hdr.appendChild(lane_mod_hdr_brand);

                    lane_mod.appendChild(lane_mod_hdr);

                    var lane_mod_stat = document.createElement("div");
                    lane_mod_stat.id = 'lane' + lane + '_module' + module['key'] + '_status';
                    lane_mod_stat.classList.add(status_bg_class[module['value']['status']]);
                    lane_mod_stat.classList.add(status_text_class[module['value']['status']]);

                    var lane_mod_stat_sym = document.createElement("span");
                    lane_mod_stat_sym.id = 'span_lane' + lane + '_module' + module['key'] + '_sym';
                    lane_mod_stat_sym.innerHTML = status_symbols[module['value']['status']];
                    lane_mod_stat.appendChild(lane_mod_stat_sym);

                    var lane_mod_stat_msg = document.createElement('span');
                    lane_mod_stat_msg.id = 'span_lane' + lane + '_module' + module['key'] + '_status';
                    lane_mod_stat_msg.classList.add('ml-2');
                    lane_mod_stat_msg.innerHTML = '<b>' + status_messages[module['value']['status']] + '</b>';
                    lane_mod_stat.appendChild(lane_mod_stat_msg);
                    lane_mod.appendChild(lane_mod_stat);


                    var lane_mod_dtg = document.createElement("div");
                    var lane_mod_dtg_id = 'lane' + lane + '_module' + module['key'] + '_dtg';
                    lane_mod_dtg.id = lane_mod_dtg_id;
                    lane_mod_dtg.classList.add('bg-gray');
                    lane_mod_dtg.classList.add('text-dark');
                    lane_mod_dtg.innerHTML = '<i>Waiting for update...</i>';
                    lane_mod.appendChild(lane_mod_dtg);

                    var lane_mod_body = document.createElement('div');
                    lane_mod_body.classList.add('card-body');
                    lane_mod_body.classList.add('pt-2');
                    lane_mod_body.classList.add('pb-0');

                    var lane_mod_body_inner = document.createElement('div');
                    lane_mod_body_inner.classList.add('row');

                    var img_src = '/static/images/T' + module['value']['mod_type'] +
                        '_V' + module['value']['mod_ver'] + '.jpg';

                    var lane_mod_loc = 'lane' + lane + '_module' + module['key'] + '_loc';

                    var lane_mod_h5 = document.createElement('h5');
                    lane_mod_h5.classList.add('col-12');
                    lane_mod_h5.classList.add('d-inline');
                    lane_mod_h5.classList.add('d-lg-none');
                    lane_mod_h5.classList.add('card-title');
                    lane_mod_h5.classList.add(lane_mod_loc);

                    var lane_mod_h5_img = document.createElement('img');
                    lane_mod_h5_img.classList.add('d-inline');
                    lane_mod_h5_img.classList.add('d-lg-none');
                    lane_mod_h5_img.classList.add('rounded');
                    lane_mod_h5_img.classList.add('float-left');
                    lane_mod_h5_img.setAttribute('src', img_src);
                    lane_mod_h5_img.setAttribute('style', 'width:50px;height:50px;transform:rotate(90deg);');
                    lane_mod_h5.appendChild(lane_mod_h5_img);

                    var lane_mod_loc_set_span = document.createElement('span');
                    lane_mod_loc_set_span.id = 'lane' + lane + '_module' + module['key'] + '_h5_span';
                    lane_mod_loc_set_span.classList.add('ml-2');
                    var fn_toggle_loc_input = 'span_clk_toggle_loc_input(' + lane + ', ' + module['key'] + ');'
                    lane_mod_loc_set_span.setAttribute('onclick', fn_toggle_loc_input);
                    lane_mod_loc_set_span.innerHTML = module['value']['loc'];

                    lane_mod_h5.appendChild(lane_mod_loc_set_span);
                    lane_mod_body_inner.appendChild(lane_mod_h5);

                    var lane_mod_h4 = document.createElement('h4');
                    lane_mod_h4.id = 'lane' + lane + '_module' + module['key'] + '_h4';
                    lane_mod_h4.classList.add('d-none');
                    lane_mod_h4.classList.add('col-12');
                    lane_mod_h4.classList.add('d-lg-inline');
                    lane_mod_h4.classList.add('d-xl-none');
                    lane_mod_h4.classList.add('card-title');
                    lane_mod_h4.classList.add(lane_mod_loc);

                    var lane_mod_h4_img = document.createElement('img');
                    lane_mod_h4_img.classList.add('d-none');
                    lane_mod_h4_img.classList.add('d-lg-inline');
                    lane_mod_h4_img.classList.add('d-xl-none');
                    lane_mod_h4_img.classList.add('rounded');
                    lane_mod_h4_img.classList.add('float-left');
                    lane_mod_h4_img.setAttribute('src', img_src);
                    lane_mod_h4_img.setAttribute('style', 'width:75px;height:75px;transform:rotate(90deg);');
                    lane_mod_h4.appendChild(lane_mod_h4_img);

                    var lane_mod_loc_set_span = document.createElement('span');
                    lane_mod_loc_set_span.id = 'lane' + lane + '_module' + module['key'] + '_h4_span';
                    lane_mod_loc_set_span.classList.add('ml-2');
                    var fn_toggle_loc_input = 'span_clk_toggle_loc_input(' + lane + ', ' + module['key'] + ');'
                    lane_mod_loc_set_span.setAttribute('onclick', fn_toggle_loc_input);
                    lane_mod_loc_set_span.innerHTML = module['value']['loc'];

                    lane_mod_h4.appendChild(lane_mod_loc_set_span);
                    lane_mod_body_inner.appendChild(lane_mod_h4);

                    var lane_mod_h3 = document.createElement('h3');
                    lane_mod_h3.id = 'lane' + lane + '_module' + module['key'] + '_h3';
                    lane_mod_h3.classList.add('col-12');
                    lane_mod_h3.classList.add('d-none');
                    lane_mod_h3.classList.add('d-xl-inline');
                    lane_mod_h3.classList.add('card-title');
                    lane_mod_h3.classList.add(lane_mod_loc);

                    var lane_mod_h3_img = document.createElement('img');
                    lane_mod_h3_img.classList.add('d-none');
                    lane_mod_h3_img.classList.add('d-xl-inline');
                    lane_mod_h3_img.classList.add('rounded');
                    lane_mod_h3_img.classList.add('float-left');
                    lane_mod_h3_img.setAttribute('src', img_src);
                    lane_mod_h3_img.setAttribute('style', 'width:100px;height:100px;transform:rotate(90deg);');
                    lane_mod_h3.appendChild(lane_mod_h3_img);

                    var lane_mod_loc_set_span = document.createElement('span');
                    lane_mod_loc_set_span.id = 'lane' + lane + '_module' + module['key'] + '_h3_span';
                    lane_mod_loc_set_span.classList.add('ml-2');
                    var fn_toggle_loc_input = 'span_clk_toggle_loc_input(' + lane + ', ' + module['key'] + ');'
                    lane_mod_loc_set_span.setAttribute('onclick', fn_toggle_loc_input);
                    lane_mod_loc_set_span.innerHTML = module['value']['loc'];

                    lane_mod_h3.appendChild(lane_mod_loc_set_span);
                    lane_mod_body_inner.appendChild(lane_mod_h3);

                    var lane_mod_body_loc = document.createElement('div');
                    lane_mod_body_loc.id = 'lane' + lane + '_module' + module['key'] + '_setloc';
                    lane_mod_body_loc.classList.add('d-none');
                    lane_mod_body_loc.classList.add('text-center');
                    lane_mod_body_loc.classList.add('mb-2');

                    var lane_mod_body_loc_text = document.createElement('input');
                    lane_mod_body_loc_text.id = 'txt_lane' + lane + '_module' + module['key'] + '_location';
                    lane_mod_body_loc_text.classList.add('form-control-sm');
                    lane_mod_body_loc_text.classList.add('col-8');
                    lane_mod_body_loc_text.classList.add('col-xl-6');
                    lane_mod_body_loc_text.classList.add('alert-info');
                    lane_mod_body_loc_text.setAttribute('type', 'text');
                    lane_mod_body_loc_text.setAttribute('placeholder', 'Location');
                    lane_mod_body_loc.appendChild(lane_mod_body_loc_text);

                    var lane_mod_body_loc_submit = document.createElement('input');
                    lane_mod_body_loc_submit.id = 'btn_lane' + lane + '_module' + module['key'] + '_location';
                    lane_mod_body_loc_submit.classList.add('ml-2');
                    lane_mod_body_loc_submit.classList.add('form-control-sm');
                    lane_mod_body_loc_submit.classList.add('btn');
                    lane_mod_body_loc_submit.classList.add('btn-info');
                    lane_mod_body_loc_submit.setAttribute('type', 'submit');
                    lane_mod_body_loc_submit.setAttribute('role', 'button');
                    var fn_mod_loc_set = 'btn_clk_module_location(' + lane + ', ' + module['key'] + ');'
                    lane_mod_body_loc_submit.setAttribute('onclick', fn_mod_loc_set);
                    lane_mod_body_loc_submit.setAttribute('onmousedown', 'event.preventDefault();');
                    lane_mod_body_loc_submit.value = 'Set';
                    lane_mod_body_loc.appendChild(lane_mod_body_loc_submit);

                    lane_mod_body_inner.appendChild(lane_mod_body_loc);
                    lane_mod_body.appendChild(lane_mod_body_inner);

                    var lane_mod_table = document.createElement("table");
                    lane_mod_table.id = 'tbl_lane' + lane + '_module' + module['key'] + '_data';
                    lane_mod_table.classList.add('col-12');
                    lane_mod_table.classList.add('mb-0');
                    lane_mod_table.classList.add('table');
                    lane_mod_table.classList.add('table-sm');
                    lane_mod_table.classList.add('table-borderless');

                    var lane_mod_table_thead = document.createElement("thead");

                    var lane_mod_table_thead_tr = document.createElement("tr");
                    lane_mod_table_thead_tr.classList.add('row');

                    var lane_mod_table_thead_tr_th = document.createElement('th');
                    lane_mod_table_thead_tr_th.id = 'th_lane' + lane + '_module' + module['key'] + '_sensor';
                    lane_mod_table_thead_tr_th.setAttribute('colspan', '2');
                    lane_mod_table_thead_tr_th.classList.add('col-12');
                    lane_mod_table_thead_tr_th.classList.add('bg-dark');
                    lane_mod_table_thead_tr_th.classList.add('text-white');
                    lane_mod_table_thead_tr_th.innerHTML = '<b>Sensors</b>';

                    var lane_mod_table_thead_tr_th_span = document.createElement('span');
                    var lane_mod_table_thead_tr_th_span_id = 'lane' + lane + '_module' + module['key'] + '_datatoggle';
                    lane_mod_table_thead_tr_th_span.id = lane_mod_table_thead_tr_th_span_id;
                    lane_mod_table_thead_tr_th_span.classList.add('pl-2');
                    lane_mod_table_thead_tr_th_span.innerHTML = '<i class="fas fa-angle-down"></i>';
                    var fn_mod_data = 'span_clk_module_data(' + lane + ', ' + module['key'] + ');'
                    lane_mod_table_thead_tr_th_span.setAttribute('onclick', fn_mod_data);
                    lane_mod_table_thead_tr_th.appendChild(lane_mod_table_thead_tr_th_span);

                    lane_mod_table_thead_tr.appendChild(lane_mod_table_thead_tr_th);
                    lane_mod_table_thead.appendChild(lane_mod_table_thead_tr);
                    lane_mod_table.appendChild(lane_mod_table_thead);

                    var lane_mod_table_tbody = document.createElement("tbody");
                    lane_mod_table_tbody.id = 'lane' + lane + '_module' + module['key'] + '_data';
                    lane_mod_table_tbody.classList.add('d-none');

                    for (sensor = 0; sensor < module['value']['num_sensors']; sensor++) {

                        var lane_mod_table_tbody_tr = document.createElement("tr");
                        lane_mod_table_tbody_tr.classList.add('row');

                        var lane_mod_table_tbody_tr_td0 = document.createElement("td");
                        var tr_td0_id = 'lane' + lane + '_module' + module['key'] + '_sensor' + sensor + '_type';
                        lane_mod_table_tbody_tr_td0.id = tr_td0_id;
                        lane_mod_table_tbody_tr_td0.classList.add('col-4');
                        lane_mod_table_tbody_tr_td0.classList.add('table-success');
                        lane_mod_table_tbody_tr_td0.classList.add('text-left');

                        var lane_mod_table_tbody_tr_td0_href = document.createElement('a');
                        lane_mod_table_tbody_tr_td0_href.classList.add('mr-2');
                        lane_mod_table_tbody_tr_td0_href.classList.add('badge');
                        lane_mod_table_tbody_tr_td0_href.classList.add('badge-info');
                        lane_mod_table_tbody_tr_td0_href.classList.add('align-middle');
                        lane_mod_table_tbody_tr_td0_href.setAttribute('data-toggle', 'modal');
                        lane_mod_table_tbody_tr_td0_href.setAttribute('data-target', '#lane' + lane + '_sensor');
                        var fn_populate_sensor_config = 'a_clk_sensor_config(' + lane + ', ' +
                            module['key'] + ', ' + sensor + ');'
                        lane_mod_table_tbody_tr_td0_href.setAttribute('onclick', fn_populate_sensor_config);
                        lane_mod_table_tbody_tr_td0_href.setAttribute('href', 'javascript:void(0);');
                        lane_mod_table_tbody_tr_td0_href.innerHTML = '<i class="fas fa-cog"></i>';
                        lane_mod_table_tbody_tr_td0.appendChild(lane_mod_table_tbody_tr_td0_href);

                        var lane_mod_table_tbody_tr_td0_small0 = document.createElement('small');
                        lane_mod_table_tbody_tr_td0_small0.classList.add('d-lg-none');
                        lane_mod_table_tbody_tr_td0_small0.innerHTML = '<b>' +
                            module['value']['S' + sensor]['type_abbr'] + '</b>';
                        lane_mod_table_tbody_tr_td0.appendChild(lane_mod_table_tbody_tr_td0_small0);

                        var lane_mod_table_tbody_tr_td0_small1 = document.createElement('small');
                        lane_mod_table_tbody_tr_td0_small1.classList.add('d-none');
                        lane_mod_table_tbody_tr_td0_small1.classList.add('d-lg-inline');
                        lane_mod_table_tbody_tr_td0_small1.innerHTML = '<b>' +
                            module['value']['S' + sensor]['type'] + '</b>';
                        lane_mod_table_tbody_tr_td0.appendChild(lane_mod_table_tbody_tr_td0_small1);

                        lane_mod_table_tbody_tr.appendChild(lane_mod_table_tbody_tr_td0);

                        var lane_mod_table_tbody_tr_td1 = document.createElement("td");
                        var tr_td1_id = 'lane' + lane + '_module' + module['key'] + '_sensor' + sensor + '_value';
                        lane_mod_table_tbody_tr_td1.id = tr_td1_id;
                        lane_mod_table_tbody_tr_td1.classList.add('col-4');
                        lane_mod_table_tbody_tr_td1.classList.add('table-info');
                        lane_mod_table_tbody_tr_td1.innerHTML = '<small>Waiting</small>';
                        lane_mod_table_tbody_tr.appendChild(lane_mod_table_tbody_tr_td1);

                        var lane_mod_table_tbody_tr_td2 = document.createElement("td");
                        var tr_td2_id = 'lane' + lane + '_module' + module['key'] + '_sensor' + sensor + '_trigger';
                        lane_mod_table_tbody_tr_td2.id = tr_td2_id;
                        lane_mod_table_tbody_tr_td2.classList.add('col-4');
                        lane_mod_table_tbody_tr_td2.classList.add('table-info');
                        lane_mod_table_tbody_tr_td2.innerHTML = '<small>Waiting</small>';
                        lane_mod_table_tbody_tr.appendChild(lane_mod_table_tbody_tr_td2);

                        lane_mod_table_tbody.appendChild(lane_mod_table_tbody_tr);
                    };

                    lane_mod_table.appendChild(lane_mod_table_tbody);
                    lane_mod_body.appendChild(lane_mod_table);

                    lane_mod.appendChild(lane_mod_body);

                    ids_lane_modules_cards[lane].appendChild(lane_mod);

                };
            };
        },
    });
};

function a_clk_sensor_config(lane, module, sensor) {

    // Gets mod_uid from hidden control
    var lane_mod_uid_id = 'lane' + lane + '_module' + module + '_mod_uid';
    var lane_mod_uid = document.getElementById(lane_mod_uid_id).value;

    var lane_sensor_btn_id = 'btn_lane' + lane + '_sensor_update';
    var lane_sensor_btn = document.getElementById(lane_sensor_btn_id);
    var fn_sensor_update = 'btn_clk_sensor_update(' + lane + ', ' + module + ', ' + sensor + ');';
    lane_sensor_btn.setAttribute('onclick', fn_sensor_update);

    var lane_trig_low_id = 'nbr_lane' + lane + '_trig_low';
    var lane_trig_low = document.getElementById(lane_trig_low_id);
    var lane_sensor_low_min_id = 'btn_lane' + lane + '_sensor_low_min';
    var lane_sensor_low_min = document.getElementById(lane_sensor_low_min_id);
    var lane_sensor_low_max_id = 'btn_lane' + lane + '_sensor_low_max';
    var lane_sensor_low_max = document.getElementById(lane_sensor_low_max_id);

    var lane_trig_high_id = 'nbr_lane' + lane + '_trig_high';
    var lane_trig_high = document.getElementById(lane_trig_high_id);
    var lane_sensor_high_min_id = 'btn_lane' + lane + '_sensor_high_min';
    var lane_sensor_high_min = document.getElementById(lane_sensor_high_min_id);
    var lane_sensor_high_max_id = 'btn_lane' + lane + '_sensor_high_max';
    var lane_sensor_high_max = document.getElementById(lane_sensor_high_max_id);

    var lane_sensor_int_id = 'nbr_lane' + lane + '_trig_int';
    var lane_sensor_int = document.getElementById(lane_sensor_int_id);

    var lane_sensor_step_id = 'nbr_lane' + lane + '_trig_step';
    var lane_sensor_step = document.getElementById(lane_sensor_step_id);

    // AJAX call to get values from server
    $.ajax({
        url: '/',
        dataType: 'json',
        data: {
            dataset: 'modconfig',
            mod_uid: lane_mod_uid,
            sensor_address: sensor
        },
        type: "GET",
        success: function ( data ) {
            lane_sensor_low_min.value = 'Min: ' + data.sensor_min + ' ' + data.sensor_unit;
            lane_sensor_low_max.value = 'Max: ' + data.sensor_max + ' ' + data.sensor_unit;
            lane_sensor_high_min.value = 'Min: ' + data.sensor_min + ' ' + data.sensor_unit;
            lane_sensor_high_max.value = 'Max: ' + data.sensor_max + ' ' + data.sensor_unit;
            lane_trig_low.value = data.trigger_baselow;
            lane_trig_low.min = data.sensor_min;
            lane_trig_low.max = data.sensor_max;
            lane_trig_high.value = data.trigger_basehigh;
            lane_trig_high.min = data.sensor_min;
            lane_trig_high.max = data.sensor_max;
            lane_sensor_int.value = data.trigger_interval;
            lane_sensor_step.value = data.trigger_step;
        },
    });
};


function span_clk_toggle_loc_input(lane, module) {
    // - Called from 'modules.js'
    // - Sets h5/h4/h3 location text display to none
    // - Sets input group elements display to block

    // Gets mod_uid from hidden control
    var lane_mod_uid_id = 'lane' + lane + '_module' + module + '_mod_uid';
    var lane_mod_uid = document.getElementById(lane_mod_uid_id).value;

    // AJAX call to get values from server
    $.ajax({
        url: '/',
        dataType: 'json',
        data: {
            dataset: 'modconfig',
            mod_uid: lane_mod_uid,
            sensor_address: 0
        },
        type: "GET",
        success: function ( data ) {

            var lane_title_h5_id = 'lane' + lane + '_module' + module + '_h5_span';
            var lane_title_h5 = document.getElementById(lane_title_h5_id);
            lane_title_h5.classList.remove('d-md-none');
            lane_title_h5.classList.add('d-none');

            var lane_title_h4_id = 'lane' + lane + '_module' + module + '_h4_span';
            var lane_title_h4 = document.getElementById(lane_title_h4_id);
            lane_title_h4.classList.remove('d-md-block');

            var lane_title_h3_id = 'lane' + lane + '_module' + module + '_h3_span';
            var lane_title_h3 = document.getElementById(lane_title_h3_id);
            lane_title_h3.classList.remove('d-xl-block');

            var txt_mod_loc_id = 'txt_lane' + lane + '_module' + module + '_location';
            txt_mod_loc = document.getElementById(txt_mod_loc_id);
            txt_mod_loc.value = data.loc;

            var lane_mod_setloc_id = 'lane' + lane + '_module' + module + '_setloc';
            lane_mod_setloc = document.getElementById(lane_mod_setloc_id);
            lane_mod_setloc.classList.remove('d-none');
        }
    });
};


function btn_clk_module_location(lane, module) {
    // - Called from 'modconfig.html/#btn_modconfig_lane_location'
    // - Collects data from 'poll.html/#txt_modconfig_lane_location' control element
    // - Posts collected data from 'poll.html/#txt_modconfig_lane_location' control element
    // - Gets values for 'poll.html/#txt_modconfig_lane_location' control and populates

    var lane_mod_uid_id = 'lane' + lane + '_module' + module + '_mod_uid';
    var lane_mod_uid = document.getElementById(lane_mod_uid_id);

    var txt_lane_mod_location_id = 'txt_lane' + lane + '_module' + module + '_location';
    txt_lane_mod_location = document.getElementById(txt_lane_mod_location_id);

    // Collect user update from 'modconfig.html/#txt_modconfig_lane_location' control element
    post_data = {
        button_name: 'location',
        mod_uid: lane_mod_uid.value,
        loc: txt_lane_mod_location.value,
    };

    // AJAX call to post collected data and return updated values from server
    $.ajax({
        url: '/',
        dataType: 'json',
        data: JSON.stringify(post_data),
        type: "POST",
        success: function ( data ) {

            var lane_mod_loc_set_span_h5_id = 'lane' + lane + '_module' + module + '_h5_span';
            var lane_mod_loc_set_span_h5 = document.getElementById(lane_mod_loc_set_span_h5_id);
            lane_mod_loc_set_span_h5.innerHTML = data.loc;
            lane_mod_loc_set_span_h5.classList.add('d-md-none');
            lane_mod_loc_set_span_h5.classList.remove('d-none');

            var lane_mod_loc_set_span_h4_id = 'lane' + lane + '_module' + module + '_h4_span';
            var lane_mod_loc_set_span_h4 = document.getElementById(lane_mod_loc_set_span_h4_id);
            lane_mod_loc_set_span_h4.innerHTML = data.loc;
            lane_mod_loc_set_span_h4.classList.add('d-md-block');

            var lane_mod_loc_set_span_h3_id = 'lane' + lane + '_module' + module + '_h3_span';
            var lane_mod_loc_set_span_h3 = document.getElementById(lane_mod_loc_set_span_h3_id);
            lane_mod_loc_set_span_h3.innerHTML = data.loc;
            lane_mod_loc_set_span_h3.classList.add('d-xl-block');

            var mod_setloc_id = 'lane' + lane + '_module' + module + '_setloc';
            var mod_setloc = document.getElementById(mod_setloc_id);
            mod_setloc.classList.add('d-none');
        },
    });
};


function btn_clk_module_poll(lane, module) {
    // - Called from 'modules.js/lane_module_carousel()' built elements for 'modules.html/#lane*_inner'
    // - Requests polling of individual module.


    // Gets mod_uid from hidden control
    var lane_mod_uid_id = 'lane' + lane + '_module' + module + '_mod_uid';
    var lane_mod_uid = document.getElementById(lane_mod_uid_id).value;

    // All submissions require this data
    var post_data = {
        button_name: 'poll_module',
        mod_uid: lane_mod_uid,
        lane_address: lane,
        module_address: module
    };

    // AJAX call to post collected data and return updated values from server
    $.ajax({
        url: '/',
        dataType: 'json',
        data: JSON.stringify(post_data),
        type: "POST",
        success: function ( data ) {

        },
    });
};


function btn_clk_module_led(led_effect, lane, module) {
    // - Called from 'modules.js/lane_module_carousel()' built elements for 'modules.html/#lane*_inner'
    // - Requests polling of individual module.


    // Gets mod_uid from hidden control
    var lane_mod_uid_id = 'lane' + lane + '_module' + module + '_mod_uid';
    var lane_mod_uid = document.getElementById(lane_mod_uid_id).value;

    // All submissions require this data
    var post_data = {
        button_name: 'led_effect',
        mod_uid: lane_mod_uid,
        lane_address: lane,
        module_address: module,
        effect: led_effect
    };

    // AJAX call to post collected data and return updated values from server
    $.ajax({
        url: '/',
        dataType: 'json',
        data: JSON.stringify(post_data),
        type: "POST",
        success: function ( data ) {

        },
    });
};

function span_clk_module_data(lane, module) {
    var lane_mod_table_tbody_tr_th_span_id = 'lane' + lane + '_module' + module + '_datatoggle';
    var lane_mod_table_tbody_tr_th_span = document.getElementById(lane_mod_table_tbody_tr_th_span_id);
    var inner_html = lane_mod_table_tbody_tr_th_span.innerHTML;

    var module_data_id = 'lane' + lane + '_module' + module + '_data';
    var module_data = document.getElementById(module_data_id);

    var lane_mod_sensor_id = 'th_lane' + lane + '_module' + module + '_sensor';
    var lane_mod_sensor = document.getElementById(lane_mod_sensor_id);

    if (module_data.classList.contains('d-none')) {
        lane_mod_table_tbody_tr_th_span.innerHTML = '<i class="fas fa-angle-down"></i>';
        module_data.classList.remove('d-none');
        module_data.classList.add('d-block');

        lane_mod_sensor.classList.remove('bg-magenta');
        lane_mod_sensor.classList.add('bg-dark');
        lane_mod_sensor.innerHTML = '<b>Sensors</b>';

        var lane_mod_table_thead_tr_th_span = document.createElement('span');
        var lane_mod_table_thead_tr_th_span_id = 'lane' + lane + '_module' + module + '_datatoggle';
        lane_mod_table_thead_tr_th_span.id = lane_mod_table_thead_tr_th_span_id;
        lane_mod_table_thead_tr_th_span.classList.add('pl-2');
        lane_mod_table_thead_tr_th_span.innerHTML = '<i class="fas fa-angle-up"></i>';
        var fn_mod_data = 'span_clk_module_data(' + lane + ', ' + module + ');'
        lane_mod_table_thead_tr_th_span.setAttribute('onclick', fn_mod_data);
        lane_mod_sensor.appendChild(lane_mod_table_thead_tr_th_span);

    } else if (module_data.classList.contains('d-block')) {
        lane_mod_table_tbody_tr_th_span.innerHTML = '<i class="fas fa-angle-down"></i>';
        module_data.classList.remove('d-block');
        module_data.classList.add('d-none');
    };
};
