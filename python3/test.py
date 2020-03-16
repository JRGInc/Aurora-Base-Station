#!/usr/bin/env python3
__author__ = 'Larry A. Hartman'
__company__ = 'Janus Research'

# Initialize Application processes
if __name__ == '__main__':
    from shared import dbase

    # Check to determine if CouchDB is operating
    dbase.mariadb_check()
