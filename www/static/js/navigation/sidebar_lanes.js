// Author: Larry A. Hartman
// Company: Janus Research Group


function a_clk_lane_sidebar_toggle(lane) {
    // - Called from 'sidebar_home.html/#a_sidebar_home*' and 'sidebar_lanes.html/#a_sidebar_lanes*'
    // - Removes 'active' class from all 'sidebar_lanes.html/.a_sidebar_lanes' elements
    // - Adds 'active' class to 'sidebar_lanes.html/#a_sidebar_lanes(lane)'
    // - Sets display style to 'none' on all 'lane(lane)_*.html/.lanes' elements
    // - Sets display style to 'block' on 'setup.html/#lane(lane)_setup'
    // - Sets display style to 'none' on all 'index.html/.index_lane' elements
    // - Sets display style to 'block' on 'index.html/#index_lane(lane)'
    // - Gets values for 'modules.html#lane(lane)_modules' controls, builds elements and populates
    // - Sets display style to 'none' on all 'index.html/.index_document' elements
    // - Sets display style to 'block' on 'index.html/#index_lane'

    // Remove 'active' class from all 'sidebar_lanes.html/.a_sidebar_lanes' elements
    // Add 'active' class to 'sidebar_lanes.html/#a_sidebar_lanes(lane)'
    remove_class(els_a_sidebar_lanes, 'active');
    remove_class(els_a_sidebar_lanes, 'bg-violet');
    remove_class(els_a_sidebar_lanes, 'text-white');
    add_class(els_a_sidebar_lanes, 'bg-tope');
    add_class(els_a_sidebar_lanes, 'text-violet');
    ids_a_sidebar_lanes[lane].classList.remove('bg-violet');
    ids_a_sidebar_lanes[lane].classList.remove('text-violet');
    ids_a_sidebar_lanes[lane].classList.add('active');
    ids_a_sidebar_lanes[lane].classList.add('bg-violet');
    ids_a_sidebar_lanes[lane].classList.add('text-white');

    // Clear 'block' display style from 'lane(lane)_*.html/.lanes' elements
    // Adds 'block' display style to 'lane(lane)_setup.html/#lane(lane)_setup'
    disp_none(els_lanes);
    ids_lane_poll[lane].classList.remove('d-none');
    ids_lane_poll[lane].classList.add('d-block');

    // Clear 'block' display style from 'index.html/.index_lanes' elements
    // Adds 'block' display style to 'index.html/#index_lanes(lane)'
    disp_none(els_index_lanes);
    ids_index_lanes[lane].classList.remove('d-none');
    ids_index_lanes[lane].classList.add('d-block');

    // AJAX call to get 'setup.html/div' and 'modules.html#lane(lane)_modules' control values
    $.ajax({
        url: '/',
        dataType: 'json',
        data: {
            dataset: 'lanes',
            lane: lane
        },
        type: "GET",
        success: function ( data ) {

            if (data.status <= 3) {

                ids_lane_modules[lane].classList.remove('d-none');
                ids_lane_modules[lane].classList.add('d-block');
            };
        },
    });

    // Clear 'block' display style from 'index.html/.index_document' elements
    // Adds 'block' display style to 'index.html/#index_lane'
    disp_none(els_index_document);
    index_lanes.classList.remove('d-none');
    index_lanes.classList.add('d-block');
};


function span_sidebar_lanes_mods_status(lane) {
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

            for (dict = 0; dict < mod_data.length; dict++) {
                if (mod_data[dict]['value']['status'] = lane_setup_id) {

                };
            };
        }
    });
};