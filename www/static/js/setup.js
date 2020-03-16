// Author: Larry A. Hartman
// Company: Janus Research Group


function setup() {
    // - Called from 'index.html' bottom of page
    // - Gets and populates values for document/head and navbar titles
    // - Adds 'active' class to 'navbar.html/#li_navbar_status'
    // - Sets display style to 'none' on all 'index.html/.index_document' elements
    // - Sets display style to 'block' on 'settings.html/#index_status'
    // - Sets display style to 'none' on all 'settings.html/.settings' elements
    // - Sets display style to 'block' on 'settings.html/#setting_core'
    // - Sets display style to 'none' on all 'chan_*.html/.channels' elements

    // AJAX call to update 'index.html/#index_title' and 'navbar.html/#navbar_title'
    $.ajax({
        dataType: 'json',
        url: '/',
        data: {dataset: 'core'},
        type: "GET",
        success: function ( data ) {
            // Update document/head and navbar titles
            update_titles(data);
        },
    });

    // Add 'active' class to 'navbar.html/#li_navbar_lanes'
    li_navbar_lanes.classList.add('active');
    li_navbar_lanes.classList.remove('btn-outline-primary');
    li_navbar_lanes.classList.add('btn-outline-success');

    // Clear 'block' display style from 'index.html/.index_document' elements
    // Adds 'block' display style to 'settings.html/#index_lanes'
    disp_none(els_index_document);
    index_lanes.classList.remove('d-none');
    index_lanes.classList.add('d-block');
    a_clk_lane_sidebar_toggle(0);

    // Clear 'block' display style from 'settings.html/.settings' elements
    // Adds 'block' display style to 'settings.html/#settings_core'
    disp_none(els_settings);
    settings_core.classList.remove('d-none');
    settings_core.classList.add('d-block');

    // Activate tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });
};