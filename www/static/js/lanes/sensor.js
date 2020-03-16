// Author: Larry A. Hartman
// Company: Janus Research Group

function btn_clk_sensor_update(lane, module, sensor) {
    // - Called from 'sensor.html/#btn_clk_sensor_update'
    // - Collects data from 'sensor.html' sensor control elements
    // - Posts collected data from 'sensor.html' sensor control element
    // - Gets values for 'sensor.htmlclassList.add('d-block');' sensor control and populates


    // Gets mod_uid from hidden control
    var lane_mod_uid_id = 'lane' + lane + '_module' + module + '_mod_uid';
    var lane_mod_uid = document.getElementById(lane_mod_uid_id).value;

    var lane_trig_low_id = 'nbr_lane' + lane + '_trig_low';
    var lane_trig_low = document.getElementById(lane_trig_low_id);

    var lane_trig_high_id = 'nbr_lane' + lane + '_trig_high';
    var lane_trig_high = document.getElementById(lane_trig_high_id);

    var lane_sensor_int_id = 'nbr_lane' + lane + '_trig_int';
    var lane_sensor_int = document.getElementById(lane_sensor_int_id);

    var lane_sensor_step_id = 'nbr_lane' + lane + '_trig_step';
    var lane_sensor_step = document.getElementById(lane_sensor_step_id);

    // Collect user data
    sensor_low_raw = lane_trig_low.value;
    sensor_high_raw = lane_trig_high.value;
    sensor_step_raw = lane_sensor_step.value;
    sensor_int_raw = lane_sensor_int.value;
    sensor_min = Number(lane_trig_low.min);
    sensor_max = Number(lane_trig_high.max);

    var valid_nbr = true;
    if (!validate_nbr(lane_trig_low, sensor_low_raw, 'low trigger')) {
        valid_nbr = false;
    };
    if (!validate_nbr(lane_trig_high, sensor_high_raw, 'high trigger')) {
        valid_nbr = false;
    };
    if (!validate_nbr(lane_sensor_step, sensor_step_raw, 'trigger step')) {
        valid_nbr = false;
    };
    if (!validate_nbr(lane_sensor_int, sensor_int_raw, 'trigger interval')) {
        valid_nbr = false;
    };

    // Five conditions for invalid user input:
    // 1. sensor_low_raw is '' (text in number field returns '')
    // 2. sensor_high_raw is '' (text in number field returns '')
    // 3. sensor_low_nbr < sensor_min
    // 4. sensor_low_nbr > sensor_max
    // 5. sensor_high_nbr < sensor_min
    // 6. sensor_high_nbr > sensor_max
    // 7. sensor_low_nbr >= sensor_high_nbr
    // 8. sensor_int_raw is '' (text in number field returns '')
    // 9. sensor_step_raw is '' (text in number field returns '')
    // 10. sensor_int_nbr <= 0
    // 11. sensor_step_nbr <= 0

    var valid_eval = true;

    if (valid_nbr) {
        sensor_low = Number(lane_trig_low.value);
        sensor_high = Number(lane_trig_high.value);
        sensor_step = Number(lane_sensor_step.value);
        sensor_int = Number(lane_sensor_int.value);

        if (sensor_low < sensor_min) {

            lane_trig_low.classList.remove('alert-info');
            lane_trig_low.classList.add('alert-warning');
            lane_trig_low.classList.add('text-danger');
            invalid_alert('Trigger low value is lower than sensor minimum capability!');
            valid_eval = false;
        };
        if (sensor_low > sensor_max) {
            lane_trig_low.classList.remove('alert-info');
            lane_trig_low.classList.add('alert-warning');
            lane_trig_low.classList.add('text-danger');
            invalid_alert('Trigger low value is higher than sensor maximum capability!');
            valid_eval = false;
        };
        if (sensor_high < sensor_min) {
            lane_trig_high.classList.remove('alert-info');
            lane_trig_high.classList.add('alert-warning');
            lane_trig_high.classList.add('text-danger');
            invalid_alert('Trigger high value is lower than sensor minimum capability!');
            valid_eval = false;
        };
        if (sensor_high > sensor_max) {
            lane_trig_high.classList.remove('alert-info');
            lane_trig_high.classList.add('alert-warning');
            lane_trig_high.classList.add('text-danger');
            invalid_alert('Trigger high value is higher than sensor maximum capability!');
            valid_eval = false;
        };
        if (sensor_low >= sensor_high) {
            lane_trig_low.classList.remove('alert-info');
            lane_trig_low.classList.add('alert-warning');
            lane_trig_low.classList.add('text-danger');
            lane_trig_high.classList.remove('alert-info');
            lane_trig_high.classList.add('alert-warning');
            lane_trig_high.classList.add('text-danger');
            invalid_alert('Trigger low value is the same or higher than trigger high value!');
            valid_eval = false;
        }

        if (valid_eval) {

            // Clear any previous data invalidation indicators if data is valid
            lane_trig_low.classList.remove('alert-warning');
            lane_trig_low.classList.remove('text-danger');
            lane_trig_low.classList.add('alert-info');
            lane_trig_high.classList.remove('alert-warning');
            lane_trig_high.classList.remove('text-danger');
            lane_trig_high.classList.add('alert-info');
            lane_sensor_int.classList.remove('alert-warning');
            lane_sensor_int.classList.remove('text-danger');
            lane_sensor_int.classList.add('alert-info');
            lane_sensor_step.classList.remove('alert-warning');
            lane_sensor_step.classList.remove('text-danger');
            lane_sensor_step.classList.add('alert-info');

            // Collect user update from 'modconfig.html' control elements
            post_data = {
                button_name: 'modconfig',
                lane_address: lane,
                mod_uid: lane_mod_uid,
                module_address: module,
                sensor_address: sensor,
                trig_low: sensor_low,
                trig_high: sensor_high,
                trig_int: sensor_int,
                trig_step: sensor_step
            };

            // AJAX call to post collected data and return updated values from server
            $.ajax({
                url: '/',
                dataType: 'json',
                data: JSON.stringify(post_data),
                type: "POST",
                success: function ( data ) {
                    lane_trig_low.value = data.trig_low;
                    lane_trig_high.value = data.trig_high;
                    lane_sensor_int.value = data.trig_int;
                    lane_sensor_step.value = data.trig_step;

                    update_alert('Values for sensor ' + sensor + ' successfully updated!');
                },
            });
        };
    };
};