#!/usr/bin/python
#
# Author:
# Henri Doreau <henri.doreau@greenbone.net>
#
# Copyright:
# Copyright (C) 2011 Greenbone Networks GmbH, http://www.greenbone.net
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2
# (or any later version), as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA.
##


"""cpelab CLI internals"""


import sys

from cpelab.databases.nmapos import NmapOS
from cpelab.databases.cpedict import CPEDict


# List of available databases
DB_MAP = {NmapOS.str_id: NmapOS, CPEDict.str_id: CPEDict}


class LabCLI:
    """this class implements cpelab base methods for interaction with the
    supported databases.
    """
    def __init__(self, args=sys.argv):
        """instanciate a new CLI"""
        self._args = args
        self.run_cmd()

    def run_cmd(self):
        """quickly parse command line and execute desired actions"""
        if self._args[1] == 'update':
            self._cmd_update(self._args[2])
        elif self._args[1] == 'stats':
            self._cmd_stats(sys.argv[2])
        elif self._args[1] == 'search':
            self._cmd_search(self._args[2], self._args[3])
        else:
            raise LabCLIError('Invalid command line')

    def _cmd_update(self, db):
        """update existing DB (or create them)"""
        for db_ref in db_iter(db):
            db_ref.create_or_update()

    def _cmd_stats(self, db):
        """compute and display statistics about existing databases"""
        for db_ref in db_iter(db):
            db_ref().display_info()

    def _cmd_search(self, item, db):
        """look for a given pattern in the selected database"""
        for db_ref in db_iter(db):
            res = db_ref().lookup(item)
            if len(res) == 0:
                print '%s: nothing found' % db_ref.str_id
            else:
                print '%s:' % db_ref.str_id
                for match in res:
                    print '%s' % str(match)

class LabCLIError(Exception):
    """base exception raised on CLI execution errors"""

def db_iter(db_spec):
    """iterate over a selection of databases"""
    if db_spec != 'all' and not DB_MAP.has_key(db_spec):
        raise LabCLIError('Invalid DB name: %s' % db_spec)

    for k, v in DB_MAP.iteritems():
        if db_spec == k or db_spec == 'all':
            yield v


def usage(reason=''):
    """print usage hint and exit"""
    sys.exit("""%s
Usage: cpelab [cmd] <parameters>
commands:
  update <db>         Download latest versions of the selected db
  stats  <db>         Display statistics about installed db
  search <item> <db>  Look for entries matching <item> in <db>

available databases: %s all""" % (reason, ' '.join(DB_MAP.keys())))

def main():
    """cpelab CLI entry point"""
    if len(sys.argv) < 2:
        usage()

    try:
        LabCLI()
    except LabCLIError, err:
        usage(err)

