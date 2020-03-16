// Author: Larry A. Hartman
// Company: Janus Research Group


function a_clk_navbar_toggle(selection) {
    // - Called from 'navbar.html/#a_navbar_(selection)'
    // - Removes 'active' class from all 'index.html/.index_document' elements
    // - Adds 'active' class to 'index.html/#index_(selection)'
    // - Sets display style to 'none' on all 'index.html/.index_document' elements
    // - Sets display style to 'block' on 'settings.html/#index_(selection)'
    // - Gets values for 'settings.html#settings_core' controls and populates
    // - Removes 'active' class from all 'settings.html/.settings' elements
    // - Adds 'active' class to 'settings.html/#settings_core'
    // - Sets display style to 'none' on all 'settings.html/.settings' elements
    // - Sets display style to 'block' on 'settings.html/#setting_core'


    // Remove 'active' class from all 'navbar.html/.li_navbar' elements
    // Add 'active' class to 'navbar.html/#li_navbar_selection'
    remove_class(els_li_navbar, 'active');
    remove_class(els_li_navbar, 'btn-outline-primary');
    remove_class(els_li_navbar, 'btn-outline-success');
    add_class(els_li_navbar, 'btn-outline-primary');
    ids_li_navbar[selection].classList.add('active');
    ids_li_navbar[selection].classList.remove('btn-outline-primary');
    ids_li_navbar[selection].classList.add('btn-outline-success');

    // Clear 'block' display style from 'index.html/.index_document' elements
    // Adds 'block' display style to 'settings.html/#index_selection'
    disp_none(els_index_document);
    ids_index[selection].classList.remove('d-none');
    ids_index[selection].classList.add('d-block');

    if (selection == 'lanes') {
        a_clk_lane_sidebar_toggle(0);
    };

    if (selection == 'settings') {
        a_clk_sidebar_settings_toggle('core');
    };

    if (selection == 'search') {


    }
};

function btn_clk_navbar_restart() {
    // - Called from 'navbar.html/System Shutdown button'

    $.confirm({
        title: 'System Restart',
        content: 'Restart the system now?',
        buttons: {
            confirm: {
                btnClass: 'btn-danger text-warning',
                action: function() {
                    $.alert({
                        title: 'System Restart',
                        content: 'System restart will commence immediately!',
                        buttons: {
                            ok: {
                                btnClass: 'btn-danger text-warning'
                            }
                        }
                    });
                    $.ajax({
                        url: '/',
                        dataType: 'json',
                        data: JSON.stringify({button_name: 'restart'}),
                        type: "POST"
                    });
                }
            },
            cancel: {
                btnClass: 'btn-primary',
                action: function() {
                    $.alert({
                        title: 'System Restart',
                        content: 'System restart was canceled.',
                        buttons: {
                            ok: {
                                btnClass: 'btn-primary'
                            }
                        }
                    });
                }
            }
        }
    });

};

function btn_clk_navbar_shutdown() {
    // - Called from 'navbar.html/System Shutdown button'

    $.confirm({
        title: 'System Shutdown',
        content: 'Shutdown the system now?',
        buttons: {
            confirm: {
                btnClass: 'btn-danger text-warning',
                action: function() {
                    $.alert({
                        title: 'System Shutdown',
                        content: 'System shutdown will commence immediately!',
                        buttons: {
                            ok: {
                                btnClass: 'btn-danger text-warning'
                            }
                        }
                    });
                    $.ajax({
                        url: '/',
                        dataType: 'json',
                        data: JSON.stringify({button_name: 'shutdown'}),
                        type: "POST"
                    });
                }
            },
            cancel: {
                btnClass: 'btn-primary',
                action: function() {
                    $.alert({
                        title: 'System Shutdown',
                        content: 'System shutdown was canceled.',
                        buttons: {
                            ok: {
                                btnClass: 'btn-primary'
                            }
                        }
                    });
                }
            }
        }
    });

};