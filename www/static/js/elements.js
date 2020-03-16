// Author: Larry A. Hartman
// Company: Janus Research Group


// Operations in index.html

// - Set obj var for 'id_title'
// - Set obj var for 'index_document'
// - Set obj vars for 'index_*'
// - Create 'ids_index' dict for access to 'index_*' obj vars
var index_title = document.getElementById('index_title');
var els_index_document = document.querySelectorAll('.index_document');
els_index_document = els_index_document.length ? els_index_document : [els_index_document];
var index_lanes = document.getElementById('index_lanes');
var index_status = document.getElementById('index_status');
var index_settings = document.getElementById('index_settings');
var index_profiles = document.getElementById('index_profiles');
var index_help = document.getElementById('index_help');
var index_search = document.getElementById('index_search');
var ids_index = {
    'lanes': index_lanes,
    'status': index_status,
    'settings': index_settings,
    'profiles': index_profiles,
    'help': index_help,
    'search': index_search
};

// - Set obj var for 'index_lanes'
// - Set obj vars for 'index_lanes*'
// - Create 'ids_index_lanes' dict for access to 'index_lanes*' obj vars
var els_index_lanes = document.querySelectorAll('.index_lanes');
els_index_lanes = els_index_lanes.length ? els_index_lanes : [els_index_lanes];
var index_lanes0 = document.getElementById('index_lanes0');
var index_lanes1 = document.getElementById('index_lanes1');
var index_lanes2 = document.getElementById('index_lanes2');
var index_lanes3 = document.getElementById('index_lanes3');
var ids_index_lanes = {
    '0': index_lanes0,
    '1': index_lanes1,
    '2': index_lanes2,
    '3': index_lanes3
};


// Operations in navbar.html

// - Set obj var for 'id_navbar_title'
// - Set obj var for 'li_navbar'
// - Set obj vars for 'li_navbar_*'
// - Create 'ids_li_navbar' dict for access to 'li_navbar_*' obj vars
var navbar_title = document.getElementById('navbar_title');
var els_li_navbar = document.querySelectorAll('.li_navbar');
els_li_navbar = els_li_navbar.length ? els_li_navbar : [els_li_navbar];
var li_navbar_lanes = document.getElementById('li_navbar_lanes');
var li_navbar_status = document.getElementById('li_navbar_status');
var li_navbar_settings = document.getElementById('li_navbar_settings');
var li_navbar_profiles = document.getElementById('li_navbar_profiles');
var li_navbar_help = document.getElementById('li_navbar_help');
var li_navbar_search = document.getElementById('li_navbar_search');
var ids_li_navbar = {
    'status': li_navbar_status,
    'lanes': li_navbar_lanes,
    'settings': li_navbar_settings,
    'profiles': li_navbar_profiles,
    'help': li_navbar_help,
    'search': li_navbar_search
};


// Operations in status.html

// - Set obj vars for 'status_base_*'
// - Create 'ids_status_base' dict for access to 'status_base_*' obj vars
var status_base_network = document.getElementById('status_base_network');
var status_base_logging = document.getElementById('status_base_logging');
var status_base_email = document.getElementById('status_base_email');
var status_base_tasks = document.getElementById('status_base_tasks');
var status_base_mariadb = document.getElementById('status_base_mariadb');
var status_base_influxdb = document.getElementById('status_base_influxdb');
var status_base_file = document.getElementById('status_base_file');
var status_base_command_listener = document.getElementById('status_base_command_listener');
var status_base_interface = document.getElementById('status_base_interface');
var status_base_poll_dispatch = document.getElementById('status_base_poll_dispatch');
var status_base_poll_data = document.getElementById('status_base_poll_data');
var status_base_snmp_agent = document.getElementById('status_base_snmp_agent');
var status_base_snmp_notify = document.getElementById('status_base_snmp_notify');
var status_base_activity_receive = document.getElementById('status_base_activity_receive');
var ids_status_base = {
    'network': status_base_network,
    'logging': status_base_logging,
    'email': status_base_email,
    'tasks': status_base_tasks,
    'mariadb': status_base_mariadb,
    'influxdb': status_base_influxdb,
    'file': status_base_file,
    'command_listener': status_base_command_listener,
    'interface': status_base_interface,
    'poll_dispatch': status_base_poll_dispatch,
    'poll_data': status_base_poll_data,
    'snmp_agent': status_base_snmp_agent,
    'snmp_notify': status_base_snmp_notify,
    'activity_receive': status_base_activity_receive
};

// - Set obj vars for 'status_base_lane*_status'
// - Create 'ids_status_base_lane_status' dict for access to 'status_base_lane*_status' obj vars
var status_base_lane0_status = document.getElementById('status_base_lane0_status');
var status_base_lane1_status = document.getElementById('status_base_lane1_status');
var status_base_lane2_status = document.getElementById('status_base_lane2_status');
var status_base_lane3_status = document.getElementById('status_base_lane3_status');
var ids_status_base_lane_status = {
    '0': status_base_lane0_status,
    '1': status_base_lane1_status,
    '2': status_base_lane2_status,
    '3': status_base_lane3_status
};

// - Set obj vars for 'status_base_lane*_polling'
// - Create 'ids_status_base_lane_polling' dict for access to 'status_base_lane*_polling' obj vars
var status_base_lane0_polling = document.getElementById('status_base_lane0_polling');
var status_base_lane1_polling = document.getElementById('status_base_lane1_polling');
var status_base_lane2_polling = document.getElementById('status_base_lane2_polling');
var status_base_lane3_polling = document.getElementById('status_base_lane3_polling');
var ids_status_base_lane_polling = {
    '0': status_base_lane0_polling,
    '1': status_base_lane1_polling,
    '2': status_base_lane2_polling,
    '3': status_base_lane3_polling
};


// Operations in sidebar_settings.html

// - Set obj var for 'a_sidebar_settings'
// - Set obj vars for 'a_sidebar_settings_*'
// - Create 'ids_a_sidebar_settings' dict for access to 'sidebar_settings_*' obj vars
var els_a_sidebar_settings = document.querySelectorAll('.a_sidebar_settings');
els_a_sidebar_settings = els_a_sidebar_settings.length ? els_a_sidebar_settings : [els_a_sidebar_settings];
var a_sidebar_settings_core = document.getElementById('a_sidebar_settings_core');
var a_sidebar_settings_dataunits = document.getElementById('a_sidebar_settings_dataunits');
var a_sidebar_settings_log = document.getElementById('a_sidebar_settings_log');
var a_sidebar_settings_compact = document.getElementById('a_sidebar_settings_compact');
var a_sidebar_settings_update = document.getElementById('a_sidebar_settings_update');
var a_sidebar_settings_cloud = document.getElementById('a_sidebar_settings_cloud');
var a_sidebar_settings_network = document.getElementById('a_sidebar_settings_network');
var a_sidebar_settings_email = document.getElementById('a_sidebar_settings_email');
var a_sidebar_settings_sms = document.getElementById('a_sidebar_settings_sms');
var a_sidebar_settings_snmp = document.getElementById('a_sidebar_settings_snmp');
var ids_a_sidebar_settings = {
    'core': a_sidebar_settings_core,
    'dataunits': a_sidebar_settings_dataunits,
    'log': a_sidebar_settings_log,
    'compact': a_sidebar_settings_compact,
    'update': a_sidebar_settings_update,
    'cloud': a_sidebar_settings_cloud,
    'network': a_sidebar_settings_network,
    'email': a_sidebar_settings_email,
    'sms': a_sidebar_settings_sms,
    'snmp': a_sidebar_settings_snmp
};


// Operations in settings.html

// - Set obj var for 'settings'
// - Set obj vars for 'settings_*'
// - Create 'ids_settings' dict for access to 'settings_*' obj vars
var els_settings = document.querySelectorAll('.settings');
els_settings = els_settings.length ? els_settings : [els_settings];
var settings_core = document.getElementById('settings_core');
var settings_dataunits = document.getElementById('settings_dataunits');
var settings_log = document.getElementById('settings_log');
var settings_compact = document.getElementById('settings_compact');
var settings_update = document.getElementById('settings_update');
var settings_cloud = document.getElementById('settings_cloud');
var settings_network = document.getElementById('settings_network');
var settings_email = document.getElementById('settings_email');
var settings_sms = document.getElementById('settings_sms');
var settings_snmp = document.getElementById('settings_snmp');
var ids_settings = {
    'core': settings_core,
    'dataunits': settings_dataunits,
    'log': settings_log,
    'compact': settings_compact,
    'update': settings_update,
    'cloud': settings_cloud,
    'network': settings_network,
    'email': settings_email,
    'sms': settings_sms,
    'snmp': settings_snmp
};

// - Set obj vars for 'settings_core' controls
var settings_core_sysname = document.getElementById('txt_settings_core_sysname');
var settings_core_customerid = document.getElementById('txt_settings_core_customerid');
var settings_core_swver = document.getElementById('txt_settings_core_swver');
var settings_core_iface = document.getElementById('txt_settings_core_iface');
var settings_core_mmap = document.getElementById('txt_settings_core_mmap');

// - Set obj vars for 'lb_settings_dataunits_temp'
// - Set obj vars for 'lbl_settings_dataunits_temp#'
// - Create 'ids_lbl_settings_dataunits_temp' dict for access to 'lbl_settings_dataunits_temp' obj vars
// - Set obj vars for 'rad_settings_dataunits_temp'
// - Set obj vars for 'rad_settings_dataunits_temp#'
// - Create 'ids_rad_settings_dataunits_temp' dict for access to 'rad_settings_dataunits_temp' obj vars
var els_lbl_settings_dataunits_temp = document.querySelectorAll('.lbl_settings_dataunits_temp');
els_lbl_settings_dataunits_temp = els_lbl_settings_dataunits_temp.length ?
    els_lbl_settings_dataunits_temp : [els_lbl_settings_dataunits_temp];
var lbl_settings_dataunits_temp0 = document.getElementById('lbl_settings_dataunits_temp0');
var lbl_settings_dataunits_temp1 = document.getElementById('lbl_settings_dataunits_temp1');
var lbl_settings_dataunits_temp2 = document.getElementById('lbl_settings_dataunits_temp2');
var ids_lbl_settings_dataunits_temp = {
    'celsius': lbl_settings_dataunits_temp0,
    'fahrenheit': lbl_settings_dataunits_temp1,
    'kelvin': lbl_settings_dataunits_temp2
};
var rad_settings_dataunits_temp = document.getElementsByName('rad_settings_dataunits_temp');
var rad_settings_dataunits_temp0 = document.getElementById('rad_settings_dataunits_temp0');
var rad_settings_dataunits_temp1 = document.getElementById('rad_settings_dataunits_temp1');
var rad_settings_dataunits_temp2 = document.getElementById('rad_settings_dataunits_temp2');
var ids_rad_settings_dataunits_temp = {
    'celsius': rad_settings_dataunits_temp0,
    'fahrenheit': rad_settings_dataunits_temp1,
    'kelvin': rad_settings_dataunits_temp2
};

// - Set obj vars for 'lbl_settings_dataunits_press'
// - Set obj vars for 'lbl_settings_dataunits_press#'
// - Create 'lb_settings_dataunits_press' dict for access to 'lbl_settings_dataunits_press' obj vars
// - Set obj var for 'rad_settings_dataunits_press'
// - Set obj vars for 'rad_settings_dataunits_press#'
// - Create 'ids_rad_settings_dataunits_press' dict for access to 'rad_settings_dataunits_press' obj vars
var els_lbl_settings_dataunits_press = document.querySelectorAll('.lbl_settings_dataunits_press');
els_lbl_settings_dataunits_press = els_lbl_settings_dataunits_press.length ?
    els_lbl_settings_dataunits_press : [els_lbl_settings_dataunits_press];
var lbl_settings_dataunits_press0 = document.getElementById('lbl_settings_dataunits_press0');
var lbl_settings_dataunits_press1 = document.getElementById('lbl_settings_dataunits_press1');
var lbl_settings_dataunits_press2 = document.getElementById('lbl_settings_dataunits_press2');
var lbl_settings_dataunits_press3 = document.getElementById('lbl_settings_dataunits_press3');
var lbl_settings_dataunits_press4 = document.getElementById('lbl_settings_dataunits_press4');
var lbl_settings_dataunits_press5 = document.getElementById('lbl_settings_dataunits_press5');
var ids_lbl_settings_dataunits_press = {
    'pascal': lbl_settings_dataunits_press0,
    'hectopascal': lbl_settings_dataunits_press1,
    'torr': lbl_settings_dataunits_press2,
    'millibar': lbl_settings_dataunits_press3,
    'atmosphere': lbl_settings_dataunits_press4,
    'psi': lbl_settings_dataunits_press5
};
var rad_settings_dataunits_press = document.getElementsByName('rad_settings_dataunits_press');
var rad_settings_dataunits_press0 = document.getElementById('rad_settings_dataunits_press0');
var rad_settings_dataunits_press1 = document.getElementById('rad_settings_dataunits_press1');
var rad_settings_dataunits_press2 = document.getElementById('rad_settings_dataunits_press2');
var rad_settings_dataunits_press3 = document.getElementById('rad_settings_dataunits_press3');
var rad_settings_dataunits_press4 = document.getElementById('rad_settings_dataunits_press4');
var rad_settings_dataunits_press5 = document.getElementById('rad_settings_dataunits_press5');
var ids_rad_settings_dataunits_press = {
    'pascal': rad_settings_dataunits_press0,
    'hectopascal': rad_settings_dataunits_press1,
    'torr': rad_settings_dataunits_press2,
    'millibar': rad_settings_dataunits_press3,
    'atmosphere': rad_settings_dataunits_press4,
    'psi': rad_settings_dataunits_press5
};

// - Set obj vars for 'lbl_settings_log_activity'
// - Set obj vars for 'lbl_settings_log#_activity'
// - Create 'lbl_settings_log_activity' dict for access to 'lbl_settings_log_activity' obj vars
// - Set obj vars for 'rad_settings_log_activity'
// - Set obj vars for 'rad_settings_log#_activity'
// - Create 'rad_settings_log_activity' dicts for access to 'rad_settings_log_activity' obj vars
var els_lbl_settings_log_activity = document.querySelectorAll('.lbl_settings_log_activity');
els_lbl_settings_log_activity = els_lbl_settings_log_activity.length ?
    els_lbl_settings_log_activity : [els_lbl_settings_log_activity];
var lbl_settings_log0_activity = document.getElementById('lbl_settings_log0_activity');
var lbl_settings_log1_activity = document.getElementById('lbl_settings_log1_activity');
var lbl_settings_log2_activity = document.getElementById('lbl_settings_log2_activity');
var lbl_settings_log3_activity = document.getElementById('lbl_settings_log3_activity');
var lbl_settings_log4_activity = document.getElementById('lbl_settings_log4_activity');
var ids_lbl_settings_log_activity = {
    'DEBUG': lbl_settings_log0_activity,
    'INFO': lbl_settings_log1_activity,
    'ERROR': lbl_settings_log2_activity,
    'WARNING': lbl_settings_log3_activity,
    'CRITICAL': lbl_settings_log4_activity
};
var rad_settings_log_activity = document.getElementsByName('rad_settings_log_activity');
var rad_settings_log0_activity = document.getElementById('rad_settings_log0_activity');
var rad_settings_log1_activity = document.getElementById('rad_settings_log1_activity');
var rad_settings_log2_activity = document.getElementById('rad_settings_log2_activity');
var rad_settings_log3_activity = document.getElementById('rad_settings_log3_activity');
var rad_settings_log4_activity = document.getElementById('rad_settings_log4_activity');
var ids_rad_settings_log_activity = {
    'DEBUG': rad_settings_log0_activity,
    'INFO': rad_settings_log1_activity,
    'ERROR': rad_settings_log2_activity,
    'WARNING': rad_settings_log3_activity,
    'CRITICAL': rad_settings_log4_activity
};

// - Set obj vars for 'lbl_settings_log_janusess'
// - Set obj vars for 'lbl_settings_log#_janusess'
// - Create 'lbl_settings_log_janusess' dict for access to 'lbl_settings_log_janusess' obj vars
// - Set obj vars for 'rad_settings_log_janusess'
// - Set obj vars for 'rad_settings_log#_janusess'
// - Create 'rad_settings_log_janusess' dicts for access to 'rad_settings_log_janusess' obj vars
var els_lbl_settings_log_janusess = document.querySelectorAll('.lbl_settings_log_janusess');
els_lbl_settings_log_janusess = els_lbl_settings_log_janusess.length ?
    els_lbl_settings_log_janusess : [els_lbl_settings_log_janusess];
var lbl_settings_log0_janusess = document.getElementById('lbl_settings_log0_janusess');
var lbl_settings_log1_janusess = document.getElementById('lbl_settings_log1_janusess');
var lbl_settings_log2_janusess = document.getElementById('lbl_settings_log2_janusess');
var lbl_settings_log3_janusess = document.getElementById('lbl_settings_log3_janusess');
var lbl_settings_log4_janusess = document.getElementById('lbl_settings_log4_janusess');
var ids_lbl_settings_log_janusess = {
    'DEBUG': lbl_settings_log0_janusess,
    'INFO': lbl_settings_log1_janusess,
    'ERROR': lbl_settings_log2_janusess,
    'WARNING': lbl_settings_log3_janusess,
    'CRITICAL': lbl_settings_log4_janusess
};
var rad_settings_log_janusess = document.getElementsByName('rad_settings_log_janusess');
var rad_settings_log0_janusess = document.getElementById('rad_settings_log0_janusess');
var rad_settings_log1_janusess = document.getElementById('rad_settings_log1_janusess');
var rad_settings_log2_janusess = document.getElementById('rad_settings_log2_janusess');
var rad_settings_log3_janusess = document.getElementById('rad_settings_log3_janusess');
var rad_settings_log4_janusess = document.getElementById('rad_settings_log4_janusess');
var ids_rad_settings_log_janusess = {
    'DEBUG': rad_settings_log0_janusess,
    'INFO': rad_settings_log1_janusess,
    'ERROR': rad_settings_log2_janusess,
    'WARNING': rad_settings_log3_janusess,
    'CRITICAL': rad_settings_log4_janusess
};

// - Set obj vars for 'lbl_settings_log_command'
// - Set obj vars for 'lbl_settings_log#_command'
// - Create 'lbl_settings_log_command' dict for access to 'lbl_settings_log_command' obj vars
// - Set obj vars for 'rad_settings_log_command'
// - Set obj vars for 'rad_settings_log#_command'
// - Create 'rad_settings_log_command' dicts for access to 'rad_settings_log_command' obj vars
var els_lbl_settings_log_command = document.querySelectorAll('.lbl_settings_log_command');
els_lbl_settings_log_command = els_lbl_settings_log_command.length ?
    els_lbl_settings_log_command : [els_lbl_settings_log_command];
var lbl_settings_log0_command = document.getElementById('lbl_settings_log0_command');
var lbl_settings_log1_command = document.getElementById('lbl_settings_log1_command');
var lbl_settings_log2_command = document.getElementById('lbl_settings_log2_command');
var lbl_settings_log3_command = document.getElementById('lbl_settings_log3_command');
var lbl_settings_log4_command = document.getElementById('lbl_settings_log4_command');
var ids_lbl_settings_log_command = {
    'DEBUG': lbl_settings_log0_command,
    'INFO': lbl_settings_log1_command,
    'ERROR': lbl_settings_log2_command,
    'WARNING': lbl_settings_log3_command,
    'CRITICAL': lbl_settings_log4_command
};
var rad_settings_log_command = document.getElementsByName('rad_settings_log_command');
var rad_settings_log0_command = document.getElementById('rad_settings_log0_command');
var rad_settings_log1_command = document.getElementById('rad_settings_log1_command');
var rad_settings_log2_command = document.getElementById('rad_settings_log2_command');
var rad_settings_log3_command = document.getElementById('rad_settings_log3_command');
var rad_settings_log4_command = document.getElementById('rad_settings_log4_command');
var ids_rad_settings_log_command = {
    'DEBUG': rad_settings_log0_command,
    'INFO': rad_settings_log1_command,
    'ERROR': rad_settings_log2_command,
    'WARNING': rad_settings_log3_command,
    'CRITICAL': rad_settings_log4_command
};

// - Set obj vars for 'lbl_settings_log_conversion'
// - Set obj vars for 'lbl_settings_log#_conversion'
// - Create 'lbl_settings_log_conversion' dict for access to 'lbl_settings_log_conversion' obj vars
// - Set obj vars for 'rad_settings_log_conversion'
// - Set obj vars for 'rad_settings_log#_conversion'
// - Create 'rad_settings_log_conversion' dicts for access to 'rad_settings_log_conversion' obj vars
var els_lbl_settings_log_conversion = document.querySelectorAll('.lbl_settings_log_conversion');
els_lbl_settings_log_conversion = els_lbl_settings_log_conversion.length ?
    els_lbl_settings_log_conversion : [els_lbl_settings_log_conversion];
var lbl_settings_log0_conversion = document.getElementById('lbl_settings_log0_conversion');
var lbl_settings_log1_conversion = document.getElementById('lbl_settings_log1_conversion');
var lbl_settings_log2_conversion = document.getElementById('lbl_settings_log2_conversion');
var lbl_settings_log3_conversion = document.getElementById('lbl_settings_log3_conversion');
var lbl_settings_log4_conversion = document.getElementById('lbl_settings_log4_conversion');
var ids_lbl_settings_log_conversion = {
    'DEBUG': lbl_settings_log0_conversion,
    'INFO': lbl_settings_log1_conversion,
    'ERROR': lbl_settings_log2_conversion,
    'WARNING': lbl_settings_log3_conversion,
    'CRITICAL': lbl_settings_log4_conversion
};
var rad_settings_log_conversion = document.getElementsByName('rad_settings_log_conversion');
var rad_settings_log0_conversion = document.getElementById('rad_settings_log0_conversion');
var rad_settings_log1_conversion = document.getElementById('rad_settings_log1_conversion');
var rad_settings_log2_conversion = document.getElementById('rad_settings_log2_conversion');
var rad_settings_log3_conversion = document.getElementById('rad_settings_log3_conversion');
var rad_settings_log4_conversion = document.getElementById('rad_settings_log4_conversion');
var ids_rad_settings_log_conversion = {
    'DEBUG': rad_settings_log0_conversion,
    'INFO': rad_settings_log1_conversion,
    'ERROR': rad_settings_log2_conversion,
    'WARNING': rad_settings_log3_conversion,
    'CRITICAL': rad_settings_log4_conversion
};

// - Set obj vars for 'lbl_settings_log_heartbeat'
// - Set obj vars for 'lbl_settings_log#_heartbeat'
// - Create 'lbl_settings_log_heartbeat' dict for access to 'lbl_settings_log_heartbeat' obj vars
// - Set obj vars for 'rad_settings_log_heartbeat'
// - Set obj vars for 'rad_settings_log#_heartbeat'
// - Create 'rad_settings_log_heartbeat' dicts for access to 'rad_settings_log_heartbeat' obj vars
var els_lbl_settings_log_heartbeat = document.querySelectorAll('.lbl_settings_log_heartbeat');
els_lbl_settings_log_heartbeat = els_lbl_settings_log_heartbeat.length ?
    els_lbl_settings_log_heartbeat : [els_lbl_settings_log_heartbeat];
var lbl_settings_log0_heartbeat = document.getElementById('lbl_settings_log0_heartbeat');
var lbl_settings_log1_heartbeat = document.getElementById('lbl_settings_log1_heartbeat');
var lbl_settings_log2_heartbeat = document.getElementById('lbl_settings_log2_heartbeat');
var lbl_settings_log3_heartbeat = document.getElementById('lbl_settings_log3_heartbeat');
var lbl_settings_log4_heartbeat = document.getElementById('lbl_settings_log4_heartbeat');
var ids_lbl_settings_log_heartbeat = {
    'DEBUG': lbl_settings_log0_heartbeat,
    'INFO': lbl_settings_log1_heartbeat,
    'ERROR': lbl_settings_log2_heartbeat,
    'WARNING': lbl_settings_log3_heartbeat,
    'CRITICAL': lbl_settings_log4_heartbeat
};
var rad_settings_log_heartbeat = document.getElementsByName('rad_settings_log_heartbeat');
var rad_settings_log0_heartbeat = document.getElementById('rad_settings_log0_heartbeat');
var rad_settings_log1_heartbeat = document.getElementById('rad_settings_log1_heartbeat');
var rad_settings_log2_heartbeat = document.getElementById('rad_settings_log2_heartbeat');
var rad_settings_log3_heartbeat = document.getElementById('rad_settings_log3_heartbeat');
var rad_settings_log4_heartbeat = document.getElementById('rad_settings_log4_heartbeat');
var ids_rad_settings_log_heartbeat = {
    'DEBUG': rad_settings_log0_heartbeat,
    'INFO': rad_settings_log1_heartbeat,
    'ERROR': rad_settings_log2_heartbeat,
    'WARNING': rad_settings_log3_heartbeat,
    'CRITICAL': rad_settings_log4_heartbeat
};

// - Set obj vars for 'lbl_settings_log_interface'
// - Set obj vars for 'lbl_settings_log#_interface'
// - Create 'lbl_settings_log_interface' dict for access to 'lbl_settings_log_interface' obj vars
// - Set obj vars for 'rad_settings_log_interface'
// - Set obj vars for 'rad_settings_log#_interface'
// - Create 'rad_settings_log_interface' dicts for access to 'rad_settings_log_interface' obj vars
var els_lbl_settings_log_interface = document.querySelectorAll('.lbl_settings_log_interface');
els_lbl_settings_log_interface = els_lbl_settings_log_interface.length ?
    els_lbl_settings_log_interface : [els_lbl_settings_log_interface];
var lbl_settings_log0_interface = document.getElementById('lbl_settings_log0_interface');
var lbl_settings_log1_interface = document.getElementById('lbl_settings_log1_interface');
var lbl_settings_log2_interface = document.getElementById('lbl_settings_log2_interface');
var lbl_settings_log3_interface = document.getElementById('lbl_settings_log3_interface');
var lbl_settings_log4_interface = document.getElementById('lbl_settings_log4_interface');
var ids_lbl_settings_log_interface = {
    'DEBUG': lbl_settings_log0_interface,
    'INFO': lbl_settings_log1_interface,
    'ERROR': lbl_settings_log2_interface,
    'WARNING': lbl_settings_log3_interface,
    'CRITICAL': lbl_settings_log4_interface
};
var rad_settings_log_interface = document.getElementsByName('rad_settings_log_interface');
var rad_settings_log0_interface = document.getElementById('rad_settings_log0_interface');
var rad_settings_log1_interface = document.getElementById('rad_settings_log1_interface');
var rad_settings_log2_interface = document.getElementById('rad_settings_log2_interface');
var rad_settings_log3_interface = document.getElementById('rad_settings_log3_interface');
var rad_settings_log4_interface = document.getElementById('rad_settings_log4_interface');
var ids_rad_settings_log_interface = {
    'DEBUG': rad_settings_log0_interface,
    'INFO': rad_settings_log1_interface,
    'ERROR': rad_settings_log2_interface,
    'WARNING': rad_settings_log3_interface,
    'CRITICAL': rad_settings_log4_interface
};

// - Set obj vars for 'lbl_settings_log_polling'
// - Set obj vars for 'lbl_settings_log#_polling'
// - Create 'lbl_settings_log_polling' dict for access to 'lbl_settings_log_polling' obj vars
// - Set obj vars for 'rad_settings_log_polling'
// - Set obj vars for 'rad_settings_log#_polling'
// - Create 'rad_settings_log_polling' dicts for access to 'rad_settings_log_polling' obj vars
var els_lbl_settings_log_polling = document.querySelectorAll('.lbl_settings_log_polling');
els_lbl_settings_log_polling = els_lbl_settings_log_polling.length ?
    els_lbl_settings_log_polling : [els_lbl_settings_log_polling];
var lbl_settings_log0_polling = document.getElementById('lbl_settings_log0_polling');
var lbl_settings_log1_polling = document.getElementById('lbl_settings_log1_polling');
var lbl_settings_log2_polling = document.getElementById('lbl_settings_log2_polling');
var lbl_settings_log3_polling = document.getElementById('lbl_settings_log3_polling');
var lbl_settings_log4_polling = document.getElementById('lbl_settings_log4_polling');
var ids_lbl_settings_log_polling = {
    'DEBUG': lbl_settings_log0_polling,
    'INFO': lbl_settings_log1_polling,
    'ERROR': lbl_settings_log2_polling,
    'WARNING': lbl_settings_log3_polling,
    'CRITICAL': lbl_settings_log4_polling
};
var rad_settings_log_polling = document.getElementsByName('rad_settings_log_polling');
var rad_settings_log0_polling = document.getElementById('rad_settings_log0_polling');
var rad_settings_log1_polling = document.getElementById('rad_settings_log1_polling');
var rad_settings_log2_polling = document.getElementById('rad_settings_log2_polling');
var rad_settings_log3_polling = document.getElementById('rad_settings_log3_polling');
var rad_settings_log4_polling = document.getElementById('rad_settings_log4_polling');
var ids_rad_settings_log_polling = {
    'DEBUG': rad_settings_log0_polling,
    'INFO': rad_settings_log1_polling,
    'ERROR': rad_settings_log2_polling,
    'WARNING': rad_settings_log3_polling,
    'CRITICAL': rad_settings_log4_polling
};

// - Set obj vars for 'lbl_settings_log_server'
// - Set obj vars for 'lbl_settings_log#_server'
// - Create 'lbl_settings_log_server' dict for access to 'lbl_settings_log_server' obj vars
// - Set obj vars for 'rad_settings_log_server'
// - Set obj vars for 'rad_settings_log#_server'
// - Create 'rad_settings_log_server' dicts for access to 'rad_settings_log_server' obj vars
var els_lbl_settings_log_server = document.querySelectorAll('.lbl_settings_log_server');
els_lbl_settings_log_server = els_lbl_settings_log_server.length ?
    els_lbl_settings_log_server : [els_lbl_settings_log_server];
var lbl_settings_log0_server = document.getElementById('lbl_settings_log0_server');
var lbl_settings_log1_server = document.getElementById('lbl_settings_log1_server');
var lbl_settings_log2_server = document.getElementById('lbl_settings_log2_server');
var lbl_settings_log3_server = document.getElementById('lbl_settings_log3_server');
var lbl_settings_log4_server = document.getElementById('lbl_settings_log4_server');
var ids_lbl_settings_log_server = {
    'DEBUG': lbl_settings_log0_server,
    'INFO': lbl_settings_log1_server,
    'ERROR': lbl_settings_log2_server,
    'WARNING': lbl_settings_log3_server,
    'CRITICAL': lbl_settings_log4_server
};
var rad_settings_log_server = document.getElementsByName('rad_settings_log_server');
var rad_settings_log0_server = document.getElementById('rad_settings_log0_server');
var rad_settings_log1_server = document.getElementById('rad_settings_log1_server');
var rad_settings_log2_server = document.getElementById('rad_settings_log2_server');
var rad_settings_log3_server = document.getElementById('rad_settings_log3_server');
var rad_settings_log4_server = document.getElementById('rad_settings_log4_server');
var ids_rad_settings_log_server = {
    'DEBUG': rad_settings_log0_server,
    'INFO': rad_settings_log1_server,
    'ERROR': rad_settings_log2_server,
    'WARNING': rad_settings_log3_server,
    'CRITICAL': rad_settings_log4_server
};

// - Set obj vars for 'lbl_settings_log_setup'
// - Set obj vars for 'lbl_settings_log#_setup'
// - Create 'lbl_settings_log_setup' dict for access to 'lbl_settings_log_setup' obj vars
// - Set obj vars for 'rad_settings_log_setup'
// - Set obj vars for 'rad_settings_log#_setup'
// - Create 'rad_settings_log_setup' dicts for access to 'rad_settings_log_setup' obj vars
var els_lbl_settings_log_setup = document.querySelectorAll('.lbl_settings_log_setup');
els_lbl_settings_log_setup = els_lbl_settings_log_setup.length ?
    els_lbl_settings_log_setup : [els_lbl_settings_log_setup];
var lbl_settings_log0_setup = document.getElementById('lbl_settings_log0_setup');
var lbl_settings_log1_setup = document.getElementById('lbl_settings_log1_setup');
var lbl_settings_log2_setup = document.getElementById('lbl_settings_log2_setup');
var lbl_settings_log3_setup = document.getElementById('lbl_settings_log3_setup');
var lbl_settings_log4_setup = document.getElementById('lbl_settings_log4_setup');
var ids_lbl_settings_log_setup = {
    'DEBUG': lbl_settings_log0_setup,
    'INFO': lbl_settings_log1_setup,
    'ERROR': lbl_settings_log2_setup,
    'WARNING': lbl_settings_log3_setup,
    'CRITICAL': lbl_settings_log4_setup
};
var rad_settings_log_setup = document.getElementsByName('rad_settings_log_setup');
var rad_settings_log0_setup = document.getElementById('rad_settings_log0_setup');
var rad_settings_log1_setup = document.getElementById('rad_settings_log1_setup');
var rad_settings_log2_setup = document.getElementById('rad_settings_log2_setup');
var rad_settings_log3_setup = document.getElementById('rad_settings_log3_setup');
var rad_settings_log4_setup = document.getElementById('rad_settings_log4_setup');
var ids_rad_settings_log_setup = {
    'DEBUG': rad_settings_log0_setup,
    'INFO': rad_settings_log1_setup,
    'ERROR': rad_settings_log2_setup,
    'WARNING': rad_settings_log3_setup,
    'CRITICAL': rad_settings_log4_setup
};

// - Set obj vars for 'lbl_settings_log_tasks'
// - Set obj vars for 'lbl_settings_log#_tasks'
// - Create 'lbl_settings_log_tasks' dict for access to 'lbl_settings_log_tasks' obj vars
// - Set obj vars for 'rad_settings_log_tasks'
// - Set obj vars for 'rad_settings_log#_tasks'
// - Create 'rad_settings_log_tasks' dicts for access to 'rad_settings_log_tasks' obj vars
var els_lbl_settings_log_tasks = document.querySelectorAll('.lbl_settings_log_tasks');
els_lbl_settings_log_tasks = els_lbl_settings_log_tasks.length ?
    els_lbl_settings_log_tasks : [els_lbl_settings_log_tasks];
var lbl_settings_log0_tasks = document.getElementById('lbl_settings_log0_tasks');
var lbl_settings_log1_tasks = document.getElementById('lbl_settings_log1_tasks');
var lbl_settings_log2_tasks = document.getElementById('lbl_settings_log2_tasks');
var lbl_settings_log3_tasks = document.getElementById('lbl_settings_log3_tasks');
var lbl_settings_log4_tasks = document.getElementById('lbl_settings_log4_tasks');
var ids_lbl_settings_log_tasks = {
    'DEBUG': lbl_settings_log0_tasks,
    'INFO': lbl_settings_log1_tasks,
    'ERROR': lbl_settings_log2_tasks,
    'WARNING': lbl_settings_log3_tasks,
    'CRITICAL': lbl_settings_log4_tasks
};
var rad_settings_log_tasks = document.getElementsByName('rad_settings_log_tasks');
var rad_settings_log0_tasks = document.getElementById('rad_settings_log0_tasks');
var rad_settings_log1_tasks = document.getElementById('rad_settings_log1_tasks');
var rad_settings_log2_tasks = document.getElementById('rad_settings_log2_tasks');
var rad_settings_log3_tasks = document.getElementById('rad_settings_log3_tasks');
var rad_settings_log4_tasks = document.getElementById('rad_settings_log4_tasks');
var ids_rad_settings_log_tasks = {
    'DEBUG': rad_settings_log0_tasks,
    'INFO': rad_settings_log1_tasks,
    'ERROR': rad_settings_log2_tasks,
    'WARNING': rad_settings_log3_tasks,
    'CRITICAL': rad_settings_log4_tasks
};

// - Set obj var for 'txt_settings_compact_*'
var txt_settings_compact_firsttime = document.getElementById('txt_settings_compact_firsttime');
var nbr_settings_compact_interval = document.getElementById('nbr_settings_compact_interval');

// - Set obj vars for 'txt_settings_update_*'
var txt_settings_update_firsttime = document.getElementById('txt_settings_update_firsttime');
var nbr_settings_update_interval = document.getElementById('nbr_settings_update_interval');

// - Set obj vars for 'chk_settings_cloud_en'
// - Set obj vars for 'btn_settings_cloud_en'
// - Set obj vars for 'txt_settings_cloud_url'
var chk_settings_cloud_en = document.getElementById('chk_settings_cloud_en');
var btn_settings_cloud_en = document.getElementById('btn_settings_cloud_en');
var txt_settings_cloud_url = document.getElementById('txt_settings_cloud_url');

// - Set obj vars for 'txt_settings_network_*'
var txt_settings_network_url = document.getElementById('txt_settings_network_url');
var nbr_settings_network_intgood = document.getElementById('nbr_settings_network_intgood');
var nbr_settings_network_intbad = document.getElementById('nbr_settings_network_intbad');
var nbr_settings_network_timeout = document.getElementById('nbr_settings_network_timeout');

// - Set obj vars for 'chk_settings_smtp_en'
// - Set obj vars for 'btn_settings_smtp_en'
var chk_settings_smtp_en = document.getElementById('chk_settings_smtp_en');
var btn_settings_smtp_en = document.getElementById('btn_settings_smtp_en');

// - Set obj vars for 'txt_settings_smtp_*'
var els_settings_smtp = document.querySelectorAll('.settings_smtp');
els_settings_smtp = els_settings_smtp.length ? els_settings_smtp : [els_settings_smtp];
var txt_settings_smtp_from = document.getElementById('txt_settings_smtp_from');
var txt_settings_smtp_server = document.getElementById('txt_settings_smtp_server');
var nbr_settings_smtp_port = document.getElementById('nbr_settings_smtp_port');
var nbr_settings_smtp_timeout = document.getElementById('nbr_settings_smtp_timeout');
var pwd_settings_smtp_pwd = document.getElementById('pwd_settings_smtp_pwd');
var txt_settings_smtp_address = document.getElementById('txt_settings_smtp_address');

// - Set obj vars for 'lbl_settings_smtp_list'
// - Set obj vars for 'lbl_settings_smtp#_list'
// - Create 'lbl_settings_smtp_list' dict for access to 'lbl_settings_smtp_list' obj vars
// - Set obj vars for 'rad_settings_smtp_list'
// - Set obj vars for 'lbl_settings_smtp#_list'
// - Create 'rad_settings_smtp_list' dicts for access to 'lbl_settings_smtp_list' obj vars
var els_lbl_settings_smtp_list = document.querySelectorAll('.lbl_settings_smtp_list');
els_lbl_settings_smtp_list = els_lbl_settings_smtp_list.length ?
    els_lbl_settings_smtp_list : [els_lbl_settings_smtp_list];
var lbl_settings_smtp0_list = document.getElementById('lbl_settings_smtp0_list');
var lbl_settings_smtp1_list = document.getElementById('lbl_settings_smtp1_list');
var lbl_settings_smtp2_list = document.getElementById('lbl_settings_smtp2_list');
var ids_lbl_settings_smtp_list = {
    'status': lbl_settings_smtp0_list,
    'alert': lbl_settings_smtp1_list,
    'error': lbl_settings_smtp2_list
};
var rad_settings_smtp_list = document.getElementsByName('rad_settings_smtp_list');
var rad_settings_smtp0_list = document.getElementById('rad_settings_smtp0_list');
var rad_settings_smtp1_list = document.getElementById('rad_settings_smtp1_list');
var rad_settings_smtp2_list = document.getElementById('rad_settings_smtp2_list');
var ids_rad_settings_smtp_list = {
    'status': rad_settings_smtp0_list,
    'alert': rad_settings_smtp1_list,
    'error': rad_settings_smtp2_list
};

// - Set obj vars for 'lbl_settings_smtp_choice'
// - Set obj vars for 'lbl_settings_smtp#_choice'
// - Create 'lbl_settings_smtp_choice' dict for access to 'lbl_settings_smtp_choice' obj vars
// - Set obj vars for 'rad_settings_smtp_choice'
// - Set obj vars for 'lbl_settings_smtp#_choice'
// - Create 'rad_settings_smtp_choice' dicts for access to 'lbl_settings_smtp_choice' obj vars
var els_lbl_settings_smtp_choice = document.querySelectorAll('.lbl_settings_smtp_choice');
els_lbl_settings_smtp_choice = els_lbl_settings_smtp_choice.length ?
    els_lbl_settings_smtp_choice : [els_lbl_settings_smtp_choice];
var lbl_settings_smtp0_choice = document.getElementById('lbl_settings_smtp0_choice');
var lbl_settings_smtp1_choice = document.getElementById('lbl_settings_smtp1_choice');
var ids_lbl_settings_smtp_choice = {
    'add': lbl_settings_smtp0_choice,
    'delete': lbl_settings_smtp1_choice,
};
var rad_settings_smtp_choice = document.getElementsByName('rad_settings_smtp_choice');
var rad_settings_smtp0_choice = document.getElementById('rad_settings_smtp0_choice');
var rad_settings_smtp1_choice = document.getElementById('rad_settings_smtp1_choice');
var ids_rad_settings_smtp_choice = {
    'add': rad_settings_smtp0_choice,
    'delete': rad_settings_smtp1_choice,
};

// - Set obj vars for 'btn_settings_smtp_list'
var btn_settings_smtp_list = document.getElementById('btn_settings_smtp_list');

// - Set obj vars for 'tbody_settings_smtp_status'
// - Set obj vars for 'tbody_settings_smtp_alert'
// - Set obj vars for 'tbody_settings_smtp_error'
var tbody_settings_smtp_status = document.getElementById('tbody_settings_smtp_status');
var tbody_settings_smtp_alert = document.getElementById('tbody_settings_smtp_alert');
var tbody_settings_smtp_error = document.getElementById('tbody_settings_smtp_error');

// - Set obj vars for 'chk_settings_sms_en'
// - Set obj vars for 'btn_settings_sms_en'
// - Set obj vars for 'txt_settings_sms_mobile'
// - Set obj vars for 'btn_settings_sms_gateways'
var chk_settings_sms_en = document.getElementById('chk_settings_sms_en');
var btn_settings_sms_en = document.getElementById('btn_settings_sms_en');
var txt_settings_sms_mobile = document.getElementById('txt_settings_sms_mobile');
var btn_settings_sms_gateways = document.getElementById('btn_settings_sms_gateways');
var dm_settings_sms_carriers = document.getElementById('dm_settings_sms_carriers');

// - Set obj vars for 'lbl_settings_sms_list'
// - Set obj vars for 'lbl_settings_sms#_list'
// - Create 'lbl_settings_sms_list' dict for access to 'lbl_settings_sms_list' obj vars
// - Set obj vars for 'rad_settings_sms_list'
// - Set obj vars for 'lbl_settings_sms#_list'
// - Create 'rad_settings_sms_list' dicts for access to 'lbl_settings_sms_list' obj vars
var els_lbl_settings_sms_list = document.querySelectorAll('.lbl_settings_sms_list');
els_lbl_settings_sms_list = els_lbl_settings_sms_list.length ?
    els_lbl_settings_sms_list : [els_lbl_settings_sms_list];
var lbl_settings_sms0_list = document.getElementById('lbl_settings_sms0_list');
var lbl_settings_sms1_list = document.getElementById('lbl_settings_sms1_list');
var lbl_settings_sms2_list = document.getElementById('lbl_settings_sms2_list');
var ids_lbl_settings_sms_list = {
    'status': lbl_settings_sms0_list,
    'alert': lbl_settings_sms1_list,
    'error': lbl_settings_sms2_list
};
var rad_settings_sms_list = document.getElementsByName('rad_settings_sms_list');
var rad_settings_sms0_list = document.getElementById('rad_settings_sms0_list');
var rad_settings_sms1_list = document.getElementById('rad_settings_sms1_list');
var rad_settings_sms2_list = document.getElementById('rad_settings_sms2_list');
var ids_rad_settings_sms_list = {
    'status': rad_settings_sms0_list,
    'alert': rad_settings_sms1_list,
    'error': rad_settings_sms2_list
};

// - Set obj vars for 'btn_settings_smtp_list'
var btn_settings_sms_list = document.getElementById('btn_settings_sms_list');

// - Set obj vars for 'tbody_settings_sms_status'
// - Set obj vars for 'tbody_settings_sms_alert'
// - Set obj vars for 'tbody_settings_sms_error'
var tbody_settings_sms_status = document.getElementById('tbody_settings_sms_status');
var tbody_settings_sms_alert = document.getElementById('tbody_settings_sms_alert');
var tbody_settings_sms_error = document.getElementById('tbody_settings_sms_error');

// - Set obj vars for 'chk_settings_snmp_agent_en'
// - Set obj vars for 'btn_settings_snmp_agent_en'
// - Set obj vars for 'chk_settings_snmp_notify_en'
// - Set obj vars for 'btn_settings_snmp_notify_en'
// - Set obj vars for 'txt_settings_snmp_*'
// - Set obj vars for 'a_settings_snmp_mib_*'
var els_settings_snmp_notify = document.querySelectorAll('.settings_snmp_notify');
els_settings_snmp_notify = els_settings_snmp_notify.length ?
    els_settings_snmp_notify : [els_settings_snmp_notify];
var chk_settings_snmp_agent_en = document.getElementById('chk_settings_snmp_agent_en');
var btn_settings_snmp_agent_en = document.getElementById('btn_settings_snmp_agent_en');
var chk_settings_snmp_notify_en = document.getElementById('chk_settings_snmp_notify_en');
var btn_settings_snmp_notify_en = document.getElementById('btn_settings_snmp_notify_en');
var txt_settings_snmp_server = document.getElementById('txt_settings_snmp_server');
var nbr_settings_snmp_port = document.getElementById('nbr_settings_snmp_port');
var txt_settings_snmp_comm = document.getElementById('txt_settings_snmp_comm');
var a_settings_snmp_mib_janus = document.getElementById('a_settings_snmp_mib_janus');
var a_settings_snmp_mib_janusess = document.getElementById('a_settings_snmp_mib_janusess');


// Operations in sidebar_lanes.html

// - Set obj var for 'a_sidebar_lanes'
// - Set obj vars for 'a_sidebar_lanes*'
// - Create 'ids_a_sidebar_lanes' dict for access to 'a_sidebar_lanes*' obj vars
var els_a_sidebar_lanes = document.querySelectorAll('.a_sidebar_lanes');
els_a_sidebar_lanes = els_a_sidebar_lanes.length ? els_a_sidebar_lanes : [els_a_sidebar_lanes];
var a_sidebar_lanes0 = document.getElementById('a_sidebar_lanes0');
var a_sidebar_lanes1 = document.getElementById('a_sidebar_lanes1');
var a_sidebar_lanes2 = document.getElementById('a_sidebar_lanes2');
var a_sidebar_lanes3 = document.getElementById('a_sidebar_lanes3');
var ids_a_sidebar_lanes = {
    '0': a_sidebar_lanes0,
    '1': a_sidebar_lanes1,
    '2': a_sidebar_lanes2,
    '3': a_sidebar_lanes3
};

// - Set obj var for 'span_sidebar_lanes_mods'
// - Set obj vars for 'span_sidebar_lanes*_mods'
// - Create 'ids_span_sidebar_lanes_mods' dict for access to 'span_sidebar_lanes*_mods' obj vars
var els_span_sidebar_lanes_mods = document.querySelectorAll('.span_sidebar_lanes_mods');
els_span_sidebar_lanes_mods = els_span_sidebar_lanes_mods.length ?
els_span_sidebar_lanes_mods : [els_span_sidebar_lanes_mods];
var span_sidebar_lanes0_mods = document.getElementById('span_sidebar_lanes0_mods');
var span_sidebar_lanes1_mods = document.getElementById('span_sidebar_lanes1_mods');
var span_sidebar_lanes2_mods = document.getElementById('span_sidebar_lanes2_mods');
var span_sidebar_lanes3_mods = document.getElementById('span_sidebar_lanes3_mods');
var ids_span_sidebar_lanes_mods = {
    '0': span_sidebar_lanes0_mods,
    '1': span_sidebar_lanes1_mods,
    '2': span_sidebar_lanes2_mods,
    '3': span_sidebar_lanes3_mods
};

// - Set obj vars for 'btn_lane*_status'
// - Create 'ids_btn_lane_status' dict for access to 'btn_lane*_status' obj vars
var btn_lane0_status = document.getElementById('btn_lane0_status');
var btn_lane1_status = document.getElementById('btn_lane1_status');
var btn_lane2_status = document.getElementById('btn_lane2_status');
var btn_lane3_status = document.getElementById('btn_lane3_status');
var ids_btn_lane_status = {
    '0': btn_lane0_status,
    '1': btn_lane1_status,
    '2': btn_lane2_status,
    '3': btn_lane3_status
};

// - Set obj vars for 'span_lane*_status'
// - Create 'ids_span_lane_status' dict for access to 'span_lane*_status' obj vars
var span_lane0_status = document.getElementById('span_lane0_status');
var span_lane1_status = document.getElementById('span_lane1_status');
var span_lane2_status = document.getElementById('span_lane2_status');
var span_lane3_status = document.getElementById('span_lane3_status');
var ids_span_lane_status = {
    '0': span_lane0_status,
    '1': span_lane1_status,
    '2': span_lane2_status,
    '3': span_lane3_status
};

// - Set obj vars for 'span_lane*_status_sym'
// - Create 'ids_span_lane_status_sym' dict for access to 'span_lane*_status_sym' obj vars
var span_lane0_status_sym = document.getElementById('span_lane0_status_sym');
var span_lane1_status_sym = document.getElementById('span_lane1_status_sym');
var span_lane2_status_sym = document.getElementById('span_lane2_status_sym');
var span_lane3_status_sym = document.getElementById('span_lane3_status_sym');
var ids_span_lane_status_sym = {
    '0': span_lane0_status_sym,
    '1': span_lane1_status_sym,
    '2': span_lane2_status_sym,
    '3': span_lane3_status_sym
};


// Operations in lanes

// - Set obj var for 'lanes'
var els_lanes = document.querySelectorAll('.lanes');
els_lanes = els_lanes.length ? els_lanes : [els_lanes];

// - Set obj vars for 'lane*_poll'
// - Create 'ids_lanes_poll' dict for access to 'lane*_poll' obj vars
var lane0_poll = document.getElementById('lane0_poll');
var lane1_poll = document.getElementById('lane1_poll');
var lane2_poll = document.getElementById('lane2_poll');
var lane3_poll = document.getElementById('lane3_poll');
var ids_lane_poll = {
    '0': lane0_poll,
    '1': lane1_poll,
    '2': lane2_poll,
    '3': lane3_poll
};

// - Set obj vars for 'lane*_modules'
// - Create 'ids_lanes_modules' dict for access to 'lane*_modules' obj vars
var lane0_modules = document.getElementById('lane0_modules');
var lane1_modules = document.getElementById('lane1_modules');
var lane2_modules = document.getElementById('lane2_modules');
var lane3_modules = document.getElementById('lane3_modules');
var ids_lane_modules = {
    '0': lane0_modules,
    '1': lane1_modules,
    '2': lane2_modules,
    '3': lane3_modules
};

// - Set obj vars for 'lane*_sensor'
// - Create 'ids_lanes_sensor' dict for access to 'lane*_sensor' obj vars
var lane0_sensor = document.getElementById('lane0_sensor');
var lane1_sensor = document.getElementById('lane1_sensor');
var lane2_sensor = document.getElementById('lane2_sensor');
var lane3_sensor = document.getElementById('lane3_sensor');
var ids_lane_sensor = {
    '0': lane0_sensor,
    '1': lane1_sensor,
    '2': lane2_sensor,
    '3': lane3_sensor
};


// Operations in poll.html


// - Set obj vars for 'btn_lane*_poll_reset'
// - Create 'ids_btn_lane_poll_reset' dict for access to 'btn_lane*_poll_reset' obj vars
var btn_lane0_reset = document.getElementById('btn_lane0_reset');
var btn_lane1_reset = document.getElementById('btn_lane1_reset');
var btn_lane2_reset = document.getElementById('btn_lane2_reset');
var btn_lane3_reset = document.getElementById('btn_lane3_reset');
var ids_btn_lane_reset = {
    '0': btn_lane0_reset,
    '1': btn_lane1_reset,
    '2': btn_lane2_reset,
    '3': btn_lane3_reset
};

// - Set obj vars for 'btn_lane*_poll_start'
// - Create 'ids_btn_lane_poll_start' dict for access to 'btn_lane*_poll_start' obj vars
var btn_lane0_poll_start = document.getElementById('btn_lane0_poll_start');
var btn_lane1_poll_start = document.getElementById('btn_lane1_poll_start');
var btn_lane2_poll_start = document.getElementById('btn_lane2_poll_start');
var btn_lane3_poll_start = document.getElementById('btn_lane3_poll_start');
var ids_btn_lane_poll_start = {
    '0': btn_lane0_poll_start,
    '1': btn_lane1_poll_start,
    '2': btn_lane2_poll_start,
    '3': btn_lane3_poll_start
};

// - Set obj vars for 'btn_lane*_poll_stop'
// - Create 'ids_btn_lane_poll_stop' dict for access to 'btn_lane*_poll_stop' obj vars
var btn_lane0_poll_stop = document.getElementById('btn_lane0_poll_stop');
var btn_lane1_poll_stop = document.getElementById('btn_lane1_poll_stop');
var btn_lane2_poll_stop = document.getElementById('btn_lane2_poll_stop');
var btn_lane3_poll_stop = document.getElementById('btn_lane3_poll_stop');
var ids_btn_lane_poll_stop = {
    '0': btn_lane0_poll_stop,
    '1': btn_lane1_poll_stop,
    '2': btn_lane2_poll_stop,
    '3': btn_lane3_poll_stop
};

// - Set obj vars for 'btn_lane*_poll_clear'
// - Create 'ids_btn_lane_poll_clear' dict for access to 'btn_lane*_poll_clear' obj vars
var btn_lane0_poll_clear = document.getElementById('btn_lane0_poll_clear');
var btn_lane1_poll_clear = document.getElementById('btn_lane1_poll_clear');
var btn_lane2_poll_clear = document.getElementById('btn_lane2_poll_clear');
var btn_lane3_poll_clear = document.getElementById('btn_lane3_poll_clear');
var ids_btn_lane_poll_clear = {
    '0': btn_lane0_poll_clear,
    '1': btn_lane1_poll_clear,
    '2': btn_lane2_poll_clear,
    '3': btn_lane3_poll_clear
};


// Operations in modules.html

// - Set obj var for 'lane_modules'
var els_lane_modules = document.querySelectorAll('.lane_modules');
els_lane_modules = els_lane_modules.length ? els_lane_modules : [els_lane_modules];

// - Set obj vars for 'lane*_modules_cards'
// - Create 'ids_lane_modules_cards' dict for access to 'lane*_modules_cards' obj vars
var lane0_modules_cards = document.getElementById('lane0_modules_cards');
var lane1_modules_cards = document.getElementById('lane1_modules_cards');
var lane2_modules_cards = document.getElementById('lane2_modules_cards');
var lane3_modules_cards = document.getElementById('lane3_modules_cards');
var ids_lane_modules_cards = {
    '0': lane0_modules_cards,
    '1': lane1_modules_cards,
    '2': lane2_modules_cards,
    '3': lane3_modules_cards
};