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
from cpelab.databases.cpedict import CPEDict

# List of available databases
DB_MAP = {NmapOS.str_id: NmapOS, CPEDict.str_id: CPEDict}


def db_iter(db_spec):
    """iterate over a selection of databases"""
    if db_spec == 'all':
        for val in DB_MAP.itervalues():
            yield val()
    else:
        yield get_db(db_spec)

def get_db(db_spec):
    """get DB by name"""
    if DB_MAP.has_key(db_spec):
        return DB_MAP[db_spec]()

