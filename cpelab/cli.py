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

from cpelab.auxiliary.auxmod import AuxModuleError
from cpelab.auxiliary.comparison import VendorDiff


# List of available databases
DB_MAP = {NmapOS.str_id: NmapOS, CPEDict.str_id: CPEDict}

# List of available processing modules
MOD_MAP = {VendorDiff.str_id: VendorDiff}


class LabCLI:
    """this class implements cpelab base methods for interaction with the
    supported databases.
    """
    def __init__(self, args=sys.argv):
        """instanciate a new CLI"""
        self._args = args
        try:
            self.run_cmd()
        except IndexError:
            raise LabCLIError('Invalid command line: missing arguments')

    def run_cmd(self):
        """quickly parse command line and execute desired actions"""
        if self._args[1] == 'update':
            self._cmd_update(self._args[2])
        elif self._args[1] == 'stats':
            self._cmd_stats(sys.argv[2])
        elif self._args[1] == 'search':
            self._cmd_search(self._args[2], self._args[3])
        elif self._args[1] == 'run':
            self._cmd_run_aux(self._args[2])
        elif self._args[1] == 'help':
            self._cmd_help_aux(self._args[2])
        else:
            raise LabCLIError('Unknown command: %s' % sys.argv[1])

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

    def _cmd_run_aux(self, modname):
        """run external processing module"""
        if not MOD_MAP.has_key(modname):
            raise LabCLIError('Unknown auxiliary module: %s' % modname)

        # Initialize and run module
        module = MOD_MAP[modname]()
        mod_args = []
        for arg in self._args[3::]:
            if not DB_MAP.has_key(arg):
                raise LabCLIError('Invalid DB name: %s' % arg)
            mod_args.append(DB_MAP[arg]())
        try:
            module.start(mod_args)
        except AuxModuleError, err:
            sys.exit(module.__class__.help_msg(err=str(err)))

    def _cmd_help_aux(self, modname):
        """display help for a specific external processing module"""
        if not MOD_MAP.has_key(modname):
            raise LabCLIError('Unknown auxiliary module: %s' % modname)

        # Initialize and run module
        module = MOD_MAP[modname]
        sys.exit(module.help_msg())

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
    dblist = ' '.join(DB_MAP.keys())
    modlist = ' '.join(MOD_MAP.keys())

    sys.exit("""%s
Usage: cpelab <cmd> <parameters...>
commands:
  update <db>         Download latest versions of the selected db
  stats  <db>         Display statistics about installed db
  search <item> <db>  Look for entries matching <item> in <db>
  run <module> <...>  Run external processing module
  help <module>       Display help for external processing module <module>

available databases: %s all
available modules: %s""" % (reason, dblist, modlist))

def main():
    """cpelab CLI entry point"""
    if len(sys.argv) < 2:
        usage()

    try:
        LabCLI()
    except LabCLIError, err:
        usage(err)

