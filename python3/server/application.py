import json
import logging
from flask import render_template, request, send_file
from server.post import config, lane, module, system
from shared import conversion, dbase

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'server'
logger = logging.getLogger(logfile)


class HandlerApp(
    object
):
    def __init__(
        self,
        flask_app
    ):
        self.flask_app = flask_app
        self.unit_convert = conversion.Conversion()

    def handler(
        self
    ):

        @self.flask_app.route('/secure/janusess.crt')
        def return_janusess_crt():
            return send_file('/opt/Janus/ESS/ssl/janusess.crt', attachment_filename='janusess.crt')

        @self.flask_app.route('/secure/janusess.cer')
        def return_janusess_cer():
            return send_file('/opt/Janus/ESS/ssl/janusess.cer', attachment_filename='janusess.cer')

        @self.flask_app.route('/snmp/mibs/JANUS-MIB')
        def return_janus_mib():
            return send_file('/opt/Janus/ESS/python3/server/snmp/mibs/JANUS-MIB', attachment_filename='JANUS-MIB')

        @self.flask_app.route('/snmp/mibs/JANUSESS-MIB')
        def return_janusess_mib():
            return send_file('/opt/Janus/ESS/python3/server/snmp/mibs/JANUSESS-MIB', attachment_filename='JANUSESS-MIB')

        @self.flask_app.route('/', methods=['GET'])
        def index_get():
            """
            Gets required data
            """
            # Determine if proper header was posted
            if request.method == 'GET':
                if request.args.get('dataset') is not None:
                    data_cdb_out = {'data': 'none'}

                    # Call relevant function
                    if request.args.get('dataset') == 'modconfig':
                        sensor = 'S{0}'.format(request.args.get('sensor_address'))

                        data0_cdb_out, stat0_cdb, http0_cdb = dbase.cdb_request(
                            cdb_cmd='get_doc',
                            cdb_name='modconfig',
                            cdb_doc=request.args.get('mod_uid'),
                            logfile=logfile
                        )

                        data1_cdb_out, stat1_cdb, http1_cdb = dbase.cdb_request(
                            cdb_cmd='get_doc',
                            cdb_name='config',
                            cdb_doc='dataunits',
                            logfile=logfile
                        )

                        if not stat0_cdb and not stat1_cdb:

                            # Check to see if sensor is installed
                            if data0_cdb_out[sensor]['id'] != 'VACANT':

                                # Convert low-threshold value to user-selected unit
                                lth_value, lth_unit = self.unit_convert.convert(
                                    data0_cdb_out[sensor]['trig_low'],
                                    data0_cdb_out[sensor]['unit'],
                                    data1_cdb_out[data0_cdb_out[sensor]['type']]
                                )

                                # Convert high-threshold value to user-selected unit
                                uth_value, uth_unit = self.unit_convert.convert(
                                    data0_cdb_out[sensor]['trig_high'],
                                    data0_cdb_out[sensor]['unit'],
                                    data1_cdb_out[data0_cdb_out[sensor]['type']]
                                )

                                # Convert step to user-selected unit
                                step_value, step_unit = self.unit_convert.convert(
                                    data0_cdb_out[sensor]['trig_step'],
                                    data0_cdb_out[sensor]['unit'],
                                    data1_cdb_out[data0_cdb_out[sensor]['type']],
                                    step=True
                                )

                                # Convert low-threshold value to user-selected unit
                                min_value, min_unit = self.unit_convert.convert(
                                    data0_cdb_out[sensor]['min'],
                                    data0_cdb_out[sensor]['unit'],
                                    data1_cdb_out[data0_cdb_out[sensor]['type']]
                                )

                                # Convert high-threshold value to user-selected unit
                                max_value, max_unit = self.unit_convert.convert(
                                    data0_cdb_out[sensor]['max'],
                                    data0_cdb_out[sensor]['unit'],
                                    data1_cdb_out[data0_cdb_out[sensor]['type']]
                                )

                                data_cdb_out = {
                                    'loc': data0_cdb_out['loc'],
                                    'mod_type': data0_cdb_out['mod_type'],
                                    'mod_ver': data0_cdb_out['mod_ver'],
                                    'num_sensors': data0_cdb_out['num_sensors'],
                                    'sensor_type': data0_cdb_out[sensor]['type'],
                                    'sensor_unit': max_unit,
                                    'sensor_min': min_value,
                                    'sensor_max': max_value,
                                    'trigger_baselow': lth_value,
                                    'trigger_basehigh': uth_value,
                                    'trigger_interval': data0_cdb_out[sensor]['trig_int'],
                                    'trigger_step': step_value
                                }

                            else:
                                data_cdb_out = {
                                    'loc': data0_cdb_out['loc'],
                                    'mod_type': data0_cdb_out['mod_type'],
                                    'mod_ver': data0_cdb_out['mod_ver'],
                                    'num_sensors': data0_cdb_out['num_sensors'],
                                    'sensor_type': 'not installed',
                                    'sensor_unit': '',
                                    'sensor_min': None,
                                    'sensor_max': None,
                                    'trigger_basehigh': None,
                                    'trigger_baselow': None,
                                    'trigger_interval': None,
                                    'trigger_step': None
                                }

                        else:
                            log = 'Could not get module configuration data ' + \
                                  'due to CouchDB error.'
                            logger.warning(log)

                    elif request.args.get('dataset') == 'modstatus':
                        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                            cdb_cmd='get_view',
                            cdb_name='modconfig',
                            cdb_doc='stat_lane{0}'.format(request.args.get('lane_address')),
                            logfile=logfile
                        )

                        if stat_cdb:
                            log = 'Could not get module configuration data ' + \
                                  'due to CouchDB error.'
                            logger.warning(log)

                    elif request.args.get('dataset') == 'lanes':
                        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                            cdb_cmd='get_doc',
                            cdb_name='lanes',
                            cdb_doc='lane{0}_status'.format(request.args.get('lane')),
                            logfile=logfile
                        )

                        if stat_cdb:
                            log = 'Could not get lane configuration data ' + \
                                  'due to CouchDB error.'
                            logger.warning(log)

                    elif request.args.get('dataset') != 'archive':
                        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
                            cdb_cmd='get_doc',
                            cdb_name='config',
                            cdb_doc=request.args.get('dataset'),
                            logfile=logfile
                        )

                        if stat_cdb:
                            log = 'Could not get base unit configuration data ' + \
                                  'due to CouchDB error.'
                            logger.warning(log)

                    return json.dumps(data_cdb_out)
            return render_template("index.html")

        @self.flask_app.route('/', methods=['POST'])
        def index_post():
            # Determine if proper header was posted
            if request.method == 'POST':

                # Process posted data
                obj_json = request.get_json(force=True)
                button_name = obj_json['button_name']

                data_cdb_out = {}
                if button_name == 'poll_start':
                    data_cdb_out = lane.poll_start(obj_json)

                elif button_name == 'poll_module':
                    data_cdb_out = module.poll(obj_json)

                elif button_name == 'poll_clear':
                    data_cdb_out = lane.poll_clear(obj_json)

                elif button_name == 'poll_stop':
                    data_cdb_out = lane.poll_stop(obj_json)

                elif button_name == 'modconfig':
                    data_cdb_out = module.modconfig(obj_json)

                elif button_name == 'reset':
                    data_cdb_out = lane.reset(obj_json)

                elif button_name == 'location':
                    data_cdb_out = module.location(obj_json)

                elif button_name == 'led_effect':
                    data_cdb_out = module.led_effect(obj_json)

                elif button_name == 'core':
                    data_cdb_out = config.core(obj_json)

                elif button_name == 'temp':
                    data_cdb_out = config.temp(obj_json)

                elif button_name == 'press':
                    data_cdb_out = config.press(obj_json)

                elif button_name == 'log':
                    data_cdb_out = config.log(obj_json)

                elif button_name == 'compact':
                    data_cdb_out = config.compact(obj_json)

                elif button_name == 'update':
                    data_cdb_out = config.update(obj_json)

                elif button_name == 'cloud':
                    data_cdb_out = config.cloud(obj_json)

                elif button_name == 'network':
                    data_cdb_out = config.network(obj_json)

                elif button_name == 'email':
                    data_cdb_out = config.email(obj_json)

                elif button_name == 'email_list':
                    data_cdb_out = config.email_list(obj_json)

                elif button_name == 'sms':
                    data_cdb_out = config.sms(obj_json)

                elif button_name == 'sms_list':
                    data_cdb_out = config.sms_list(obj_json)

                elif button_name == 'snmp':
                    data_cdb_out = config.snmp(obj_json)

                elif button_name == 'restart':
                    data_cdb_out = system.restart()

                elif button_name == 'shutdown':
                    data_cdb_out = system.shutdown()

                # Write returned data to webpage
                return json.dumps(data_cdb_out)
