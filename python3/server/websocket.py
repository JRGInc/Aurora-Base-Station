import geventwebsocket
import logging
import multiprocessing
import time
from geventwebsocket import WebSocketApplication
from shared import dbase
from shared.globals import MPQ_WS, MPQ_STAT

__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

logfile = 'server'
logger = logging.getLogger(logfile)


class HandlerWS(
    WebSocketApplication
):

    # Do not remove this overloaded method.
    def on_open(
        self
    ):
        """
        Processes to execute when websocket opens
        """
        self.mp_ws_listener = None
        self.mp_ws_listener_stop = multiprocessing.Queue(-1)
        try:
            self.listener()

        except geventwebsocket.WebSocketError:
            log = 'Websocket experienced an error on opening.'
            logger.exception(log)

    # Do not remove this overloaded method, need this to catch message sent on page
    # close/reload event.
    def on_message(
        self,
        message
    ):
        """
        Processes to execute when a websocket message is received
        """
        try:
            pass
        except geventwebsocket.WebSocketError:
            log = 'Websocket experienced an error on receiving message.'
            logger.exception(log)

    # Do not remove this overloaded method
    def on_close(
        self,
        reason
    ):
        """
        Processes to execute when websocket closes
        """
        # Ensure that multiprocess process is terminated
        if self.mp_ws_listener is not None:
            if self.mp_ws_listener.is_alive():
                self.mp_ws_listener_stop.put_nowait(None)
                time.sleep(0.1)
                if self.mp_ws_listener.is_alive():
                    self.mp_ws_listener.join()

        # Update base_pid document in CouchDB config database
        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='config',
            cdb_doc='base_pid',
            data_cdb_in={'websocket_handler': False},
            logfile=logfile
        )

        if stat_cdb:
            log = 'Could not update websocket PID values in process status document due to CouchDB error.'
            logger.warning(log)

        MPQ_STAT.put_nowait([
            'websocket',
            False
        ])

    def listener(
        self
    ):
        """
        Listener to open when a page websocket connection is established
        """
        try:
            self.mp_ws_listener = multiprocessing.Process(
                target=self.websocket,
                args=()
            )

            self.mp_ws_listener.start()
            pid_handler = self.mp_ws_listener.pid
            log = 'Flask websocket handler opened, pid: {0}.'.format(pid_handler)
            logger.info(log)

            MPQ_STAT.put_nowait([
                'websocket',
                self.mp_ws_listener.pid
            ])

        except multiprocessing.ProcessError:
            pid_handler = False
            log = 'Can not dispatch heartbeat channel encoded messages ' + \
                  'due to multiprocessing error.'
            logger.exception(log)

        data_cdb_out, stat_cdb, http_cdb = dbase.cdb_request(
            cdb_cmd='upd_doc',
            cdb_name='config',
            cdb_doc='base_pid',
            data_cdb_in={'websocket_handler': pid_handler},
            logfile=logfile
        )

        if stat_cdb:
            log = 'Could not update websocket PID values in process status document due to CouchDB error.'
            logger.warning(log)

    def websocket(
        self,
    ):
        """
        Starts websocket multiprocessing queue listener

        mpq_record[0] = type
        mpq_record[1] to mpq_record[?] = data
        """
        while True:
            # Check for loop stop/exit condition
            if not self.mp_ws_listener_stop.empty():
                message = self.mp_ws_listener_stop.get()
                if message is None:
                    break

            # Get record from queue
            if not MPQ_WS.empty():
                mpq_record = MPQ_WS.get()

                # Build message for websocket
                message = ''
                for field in mpq_record:
                    message = message + str(field) + "/"
                message = message[:-1]

                # Write message to websocket and trap any errors
                try:
                    self.ws.send(message)

                except geventwebsocket.WebSocketError:
                    MPQ_WS.put(mpq_record)
                    log = 'Can not put message on websocket due to socket closed error: key {0}, status {1}.'. \
                          format(mpq_record[0], mpq_record[1])
                    logger.exception(log)
                    print(log)
                    break

            time.sleep(0.02)
