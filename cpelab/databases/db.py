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


"""base cpelab databases manipulation module"""

import os
import sqlite3

DATADIR = 'data'
SQLITE_DB_FILE = 'cpelab.db'
SQLITE_INIT_SCRIPT = 'cpelab_init.sql'


class Database:
    """Base (abstract) class for DB. Define a common interface for subclasses"""

    str_id = None

    def __init__(self):
        """Initialize a new DB"""
        self.path = os.path.join(os.getcwd(), DATADIR, SQLITE_DB_FILE)
        self.conn = None
        self.cursor = None
        self.fields_map = {}
        self._search_fields = []

    def connect(self):
        """Open connection to the database"""
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Release connections to the database"""
        if self.cursor is None or self.conn is None:
            raise DBError('Invalid close!')

        # commit pending operations
        self.conn.commit()

        self.cursor.close()
        self.conn.close()

    def initialize(self):
        """Call the DB initialization script. Delete everything and re-create
        empty tables"""
        initfile = os.path.join(os.getcwd(), DATADIR, SQLITE_INIT_SCRIPT)
        fin = open(initfile)
        self.cursor.executescript(fin.read())
        fin.close()

    def count(self, field=None):
        """
        """
        if field is None:
            # default: count the number of items
            self.cursor.execute('select COUNT(*) from %s' % self.str_id)
            return self.cursor.fetchone()
        else:
            # count unique entries for a given field
            self.cursor.execute('select COUNT(*) from (select distinct %s from %s)' \
                % (self.dbfield(field), self.str_id))
            return self.cursor.fetchone()[0]

    def lookup(self, spec, strict=True):
        """
        """
        # TODO make a light and efficient iterator
        items = []
        if strict:
            cmp = '='
        else:
            cmp = 'like'
        
        filter = []
        elems = []
        for k, v in spec.iteritems():
            filter.append('%s %s ?' % (k, cmp))
            elems.append(v)
        filter = ' and '.join(filter)
        query = 'select * from %s where (%s)' % (self.str_id, filter)
        self.cursor.execute(query, tuple(elems))
        for res in self.cursor.fetchall():
            items.append(self._make_item(res))
        return items

    def lookup_all(self, pattern):
        """
        """
        items = []
        for field in self._search_fields:
            items += self.lookup({field: pattern}, strict=False)
        return items

    def dbfield(self, field):
        """
        """
        return self.fields_map[field]

    def _make_item(self):
        """
        """
        raise NotImplementedError('Abstract method subclasses must implement!')

class DBEntry:
    """Represent a single database item"""
    def __init__(self):
        """instanciate a new item"""
        self.fields = {}

    def save(self, db):
        """
        """
        raise NotImplementedError('Abstract method subclasses must implement')

class DBError(Exception):
    """Base error raised on invalid DB operations"""

