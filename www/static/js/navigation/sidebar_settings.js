// Author: Larry A. Hartman
// Company: Janus Research Group


function a_clk_sidebar_settings_toggle(selection) {
    // - Called from 'sidebar_settings.html/#a_sidebar_settings_(selection)'
    // - Removes 'active' class from all 'sidebar_settings.html/.a_sidebar_settings' elements
    // - Adds 'active' class to 'sidebar_settings.html/#a_sidebar_settings_(selection)'
    // - Sets display style to 'none' on all 'settings.html/.settings' elements
    // - Sets display style to 'block' on 'settings.html/#settings_(selection)'
    // - Gets values for 'settings.html#settings_selection' controls and populates

    // Remove 'active' class from all 'sidebar_settings.html/.a_sidebar_settings' elements
    // Add 'active' class to 'sidebar_settings.html/#id_a_sidebar_settings_selection'
    remove_class(els_a_sidebar_settings, 'active');
    remove_class(els_a_sidebar_settings, 'bg-violet');
    remove_class(els_a_sidebar_settings, 'text-white');
    add_class(els_a_sidebar_settings, 'bg-tope');
    add_class(els_a_sidebar_settings, 'text-violet');
    ids_a_sidebar_settings[selection].classList.remove('bg-tope');
    ids_a_sidebar_settings[selection].classList.remove('text-violet');
    ids_a_sidebar_settings[selection].classList.add('active');
    ids_a_sidebar_settings[selection].classList.add('bg-violet');
    ids_a_sidebar_settings[selection].classList.add('text-white');

    // Clear 'block' display style from 'settings.html/.settings' elements
    // Adds 'block' display style to 'settings.html/#settings_selection'
    disp_none(els_settings);
    ids_settings[selection].classList.remove('d-none');
    ids_settings[selection].classList.add('d-block');

    // AJAX call to get 'settings.html/#settings_selection' control values
    $.ajax({
        url: '/',
        dataType: 'json',
        data: {dataset: selection},
        type: "GET",
        success: function ( data ) {
            switch (selection) {
                case 'core':
                    // Update values in 'settings.html/#settings_core' controls
                    update_settings_core(data);
                    break;

                case 'dataunits':
                    // Update values in 'settings.html/#settings_dataunits' controls
                    update_settings_dataunits(data);
                    break;

                case 'log':
                    // Update values in 'settings.html/#settings_log' controls
                    update_settings_log(data);
                    break;

                case 'compact':
                    // Update values in 'settings.html/#settings_compact' controls
                    update_settings_compact(data);
                    break;

                case 'update':
                    // Update values in 'settings.html/#settings_update' controls
                    update_settings_update(data);
                    break;

                case 'cloud':
                    // Update values in 'settings.html/#settings_cloud' controls
                    update_settings_cloud(data);
                    break;

                case 'network':
                    // Update values in 'settings.html/#settings_network' controls
                    update_settings_network(data);
                    break;

                case 'email':
                    // Update values in 'settings.html/#settings_email' controls
                    update_settings_email(data);
                    update_settings_email_list(data);
                    break;

                case 'sms':
                    // Update values in 'settings.html/#settings_sms' controls
                    update_settings_sms(data);
                    update_settings_sms_list(data);
                    break;

                case 'snmp':
                    // Update values in 'settings.html/#settings_snmp' controls
                    update_settings_snmp(data);
                    break;

            };
        }
    });
};