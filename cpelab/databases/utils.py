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


"""misc database utilities"""

from cpelab.databases.nmapos import NmapOS
from cpelab.databases.cpedict import CPEOS


# List of available databases
DB_MAP = { NmapOS.str_id: NmapOS,
           CPEOS.str_id: CPEOS }


def get_db(db_spec):
    """Get a single DB by name."""
    if DB_MAP.has_key(db_spec):
        return DB_MAP[db_spec]()

class DBSpecParser:
    """Analyze a database specification pattern and provide accessors to the
    corresponding instances.
    """
    def __init__(self, pattern=None):
        """initialize a new DBSpecParser instance"""
        self._dbs = []
        if pattern == 'all':
            self._dbs = DB_MAP.values()
        else:
            for spec in pattern.split(' '):
                if DB_MAP.has_key(spec):
                    self._dbs.append(DB_MAP[spec])
                else:
                    raise DBSpecError('Invalid DB specification: %s' % pattern)

    def __iter__(self):
        """Iterate through the selected databases."""
        for val in self._dbs:
            yield val()

    def __str__(self):
        """Human readable representation of an instance."""
        return ' '.join([str(x) for x in self._dbs])

class DBSpecError(Exception):
    """Error raised for invalid DB specification patterns"""

