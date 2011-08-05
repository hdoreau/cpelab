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


"""Base cpelab databases manipulation module"""

import os
import sqlite3

DATADIR = 'data'
SQLITE_DB_FILE = 'cpelab.db'
SQLITE_INIT_SCRIPT = 'cpelab_init.sql'


class Database:
    """Base (abstract) class for DB. Define a common interface for subclasses."""

    str_id = None

    def __init__(self):
        """Initialize a new DB."""
        self.path = os.path.join(os.getcwd(), DATADIR, SQLITE_DB_FILE)
        self.db_cnx = sqlite3.connect(self.path)  # eager connection
        self.fields_map = {}
        self._search_fields = []

    def initialize(self):
        """Call the DB initialization script. Delete everything and re-create
        empty tables.
        """
        initfile = os.path.join(os.getcwd(), DATADIR, SQLITE_INIT_SCRIPT)
        fin = open(initfile)
        self.db_cnx.executescript(fin.read())
        self.db_cnx.commit()
        fin.close()

    def count(self, field=None):
        """Count the number of items or distinct entries for a given field if
        supplied.
        """
        if field is None:
            # default: count the number of items
            cursor = self.db_cnx.execute('select COUNT(*) from %s' % self.str_id)
            return cursor.fetchone()
        else:
            # count unique entries for a given field
            cursor = self.db_cnx.execute('select COUNT(*) from (select distinct %s from %s)' \
                % (self.dbfield(field), self.str_id))
            return cursor.fetchone()[0]

    def lookup(self, spec, strict=True):
        """Perform lookup queries on the database.

        spec is a dict, which keys are non db-specific fields (like 'vendor', or
        'product'), on which you want to filter, and values are the pattern that
        you want to apply on each field.

        eg;
        spec = {'vendor': 'openbsd', 'product': 'openbsd', 'version': '4.7'}

        The strict arguments allows you to choose between a strict matching mode
        ('field = value') or a more flexible one ('field like pattern').
        """
        if strict:
            op = '='
        else:
            op = 'like'
        
        search_filter = []
        elems = []
        for k, v in spec.iteritems():
            search_filter.append('%s %s ?' % (self.dbfield(k), op))
            elems.append(v)
        search_filter = ' and '.join(search_filter)
        query = 'select * from %s where (%s)' % (self.str_id, search_filter)
        for res in self.db_cnx.execute(query, tuple(elems)):
            yield self._make_item(res)

    def lookup_all(self, pattern):
        """Provided for conveniency, look for pattern on all the search-relevant
        fields of a database.
        """
        items = []
        for field in self._search_fields:
            items += self.lookup({field: pattern}, strict=False)
        return items

    def dbfield(self, field):
        """Get the internal name of a field from its application wide
        exrpession.
        """
        return self.fields_map[field]

    def _make_item(self, data):
        """Return an item (object) created from database information."""
        raise NotImplementedError('Abstract method subclasses must implement!')

class DBEntry:
    """Represent a single database item"""
    def __init__(self):
        """instanciate a new item"""
        self.fields = {}

    def save(self, db):
        """Store a new item into the database."""
        raise NotImplementedError('Abstract method subclasses must implement')

class DBError(Exception):
    """Base error raised on invalid DB operations"""

