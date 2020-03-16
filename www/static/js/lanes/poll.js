// Author: Larry A. Hartman
// Company: Janus Research Group

function btn_clk_lane_reset(lane) {
    // - Called from 'poll.html/div/submit' button
    // - Collects data from 'poll.html/div' control elements
    // - Posts collected data from 'poll.html/div' control elements
    // - Gets values for 'poll.html/div' controls and populates
    // - Sets display style to 'none' on all 'lane(lane)_*.html/.lanes' elements
    // - Sets display style to 'block' on 'lane(lane)_setup.html/#lane(lane)_setup'

    command_acknowledge('Lane ' + lane + ' reset acknowledged.');

    // Collect user updates from 'setup.html/div' control elements
    post_data = {
        button_name: 'reset',
        lane_address: lane
    };

    // AJAX call to get 'setup.html/div' and 'modules.html#lane(lane)_modules' control values
    $.ajax({
        url: '/',
        dataType: 'json',
        data: JSON.stringify(post_data),
        type: "POST",
        success: function ( data ) {
            if (data.fail == false) {

                // Clear 'block' display style from 'modules.html/.lane_carousel' elements
                // Remove elements from carousel parent div
                // Build modules carousel and display lane ids only if lane does not fail
                if (data.status <= 3) {
                	ids_lane_modules[lane].classList.remove('d-block');
                	ids_lane_modules[lane].classList.add('d-none');
                	
                    lane_module_card_deck(lane, data.setup_id, data.last_module);
                    
                    ids_lane_modules[lane].classList.remove('d-none');
                    ids_lane_modules[lane].classList.add('d-block');
                };
            };
        },
    });
};


function btn_clk_lane_poll_start(lane) {
    // - Called from 'poll.html/#btn_lane*_poll_start' submit button
    // - Collects data from 'settings.html/#settings_(button_name)' control elements
    // - Posts collected data from 'settings.html/#settings_(button_name)' control elements
    // - Gets values for 'settings.html#settings_(button_name)' controls and populates

    command_acknowledge('Polling start for lane ' + lane + ' acknowledged.');

    // 'poll_start' submission needs this addition data
    var post_data = {
        button_name: 'poll_start',
        button_lane: lane
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


function btn_clk_lane_poll_stop(lane) {
    // - Called from 'poll.html/#btn_lane*_poll_stop' submit button
    // - Posts submission to stop automated polling

    command_acknowledge('Polling stop for lane ' + lane + ' acknowledged.');

    var post_data = {
        button_name: 'poll_stop',
        button_lane: lane
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


function btn_clk_lane_poll_clear(lane) {
    // - Called from 'poll.html/#btn_lane*_poll_clear' submit button
    // - Posts submission to clear poll data from InfluxDB

    command_acknowledge('Clear polling data request for lane ' + lane + ' acknowledged.');

    var post_data = {
        button_name: 'poll_clear',
        button_lane: lane
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
