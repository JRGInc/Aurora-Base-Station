import logging
import multiprocessing
import os
from collections import OrderedDict
from geventwebsocket import WebSocketServer, Resource
from gevent.pywsgi import WSGIServer
from flask import Flask
from server.application import HandlerApp
from server.websocket import HandlerWS
from shared import dbase

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'server'
logger = logging.getLogger(logfile)


class FlaskServer(
    object
):
    def __init__(
        self
    ):
        """
        Setup Flask properties
        """
        self.mp_app = None
        self.mp_ws = None

        template_dir = os.path.realpath('/opt/Janus/ESS/www/templates')
        static_dir = os.path.realpath('/opt/Janus/ESS/www/static')
        self.flask_app = Flask(
            __name__,
            template_folder=template_dir,
            static_folder=static_dir
        )
        self.flask_app.debug = True
        self.handler_app = HandlerApp(self.flask_app)
        self.handler_app.handler()

    def application(
        self
    ):
        """
        Run main flask application, SSL handled by nginx
        """
        http_server_ws = WSGIServer(
            ('127.0.0.1',
             8889),
            self.flask_app
        )
        http_server_ws.serve_forever()

    @staticmethod
    def websocket():
        """
        Run websocket flask application, SSL handled by nginx
        """
        http_server_ws = WebSocketServer(
            ('127.0.0.1',
             8890),
            Resource(OrderedDict([('/websocket/', HandlerWS)]))
        )
        http_server_ws.serve_forever()

    def webserver(
        self
    ):
        """
        Call main and websocket applications via multiprocessing
        """
        data_cdb_in = {}

        # Start and run web server main listener
        try:
            self.mp_app = multiprocessing.Process(
                target=self.application,
                args=()
            )
            self.mp_app.start()
            log = 'Webserver application started.'
            logger.info(log)
            data_cdb_in['webserver_main'] = self.mp_app.pid

        except multiprocessing.ProcessError:
            log = 'Can not start main webserver due to multiprocessing error.'
            logger.exception(log)

        # Start and run web server websocket listener
        try:
            self.mp_ws = multiprocessing.Process(
                target=self.websocket,
                args=()
            )
            self.mp_ws.start()
            log = 'Websocket application started.'
            logger.info(log)
            data_cdb_in['webserver_websocket'] = self.mp_ws.pid

        except multiprocessing.ProcessError:
            log = 'Can not start websocket due to multiprocessing error.'
            logger.exception(log)

        # Update base_pid document in CouchDB config database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='config',
            cdb_doc='base_pid',
            data_cdb_in=data_cdb_in,
            logfile=logfile
        )

        if stat_cdb:
            log = 'Could not set PID values in process status document due to CouchDB error.'
            logger.warning(log)
