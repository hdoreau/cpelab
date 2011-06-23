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

from cpelab.databases.utils import db_iter 
from cpelab.tools.toolbase import RuntimeToolError, UpdateDB, StatsDB, SearchDB
from cpelab.tools.comparison import VendorDiff


# List of available processing modules
TOOLS_MAP = {
    UpdateDB.str_id: UpdateDB,
    StatsDB.str_id: StatsDB,
    SearchDB.str_id: SearchDB,
    VendorDiff.str_id: VendorDiff
}


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
        cmd = self._args[1]

        if cmd == 'help':
            # specific case for help, which is not implemented as a tool
            sys.exit(self._cmd_help(self._args[2]))

        if not TOOLS_MAP.has_key(cmd):
            raise LabCLIError('Unknown command: %s' % cmd)

        tool = TOOLS_MAP[cmd]
        try:
            tool().start(self._args[2::])
        except RuntimeToolError, err:
            sys.exit(tool.help_msg(err=str(err)))

    def _cmd_help(self, modname):
        """display help for a specific external processing module"""
        if TOOLS_MAP.has_key(modname):
            return TOOLS_MAP[modname].help_msg()
        raise LabCLIError('Unknown command: %s' % modname)

class LabCLIError(Exception):
    """base exception raised on CLI execution errors"""


def usage(reason=''):
    """print usage hint and exit"""
    dblist = ' '.join([x.str_id for x in db_iter('all')])
    modlist = '\n  '.join(TOOLS_MAP.keys())

    sys.exit("""%s
Usage: cpelab <cmd> [parameters...]
commands:
  help <modname>  Display help for a given command

  %s

available databases: %s all""" % (reason, modlist, dblist))

def main():
    """cpelab CLI entry point"""
    if len(sys.argv) < 2:
        usage()

    try:
        LabCLI()
    except LabCLIError, err:
        usage(err)

