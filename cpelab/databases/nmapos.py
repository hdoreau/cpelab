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


"""Nmap OS database manipulation module"""

import urllib2

from cpelab.databases.db import Database, DBEntry


NMAP_OS_DICT_LOCATION = 'http://nmap.org/svn/nmap-os-db'


class NmapOS(Database):
    """Nmap OS fingerprints database."""

    str_id = 'nmapos'

    def __init__(self):
        """Initialize a new Nmap OS DB instance"""
        Database.__init__(self)
        self._item_title = None
        self.fields_map = {
            'title': 'n_title',
            'vendor': 'n_vendor',
            'product': 'n_product',
            'version': 'n_version',
            'devtype': 'n_devtype'
        }
        self._search_fields = ['title']

    def populate(self):
        """Download latest version of the database from a remote location and
        store it locally.
        """
        print '[+] Updating %s...' % str(NmapOS.str_id)

        self.connect()
        full_db = urllib2.urlopen(NMAP_OS_DICT_LOCATION)

        print '[+] Storing base...'

        tmp_item = None
        for line in full_db:
            if line.startswith('Fingerprint'):
                tmp_item = NmapOSItem()
                tmp_item.update(line)
            elif line.startswith('Class'):
                tmp_item.update(line)
                if tmp_item is not None:
                    tmp_item.save(self)

        self.close()

        # XXX display statistics
        print '[+] Update complete!'

    def _make_item(self, data):
        """Create and return an item (object) from database information."""
        item = NmapOSItem()
        # data[0] is the DB id, discard it
        item.fields['title'] = data[1]
        item.fields['vendor'] = data[2]
        item.fields['product'] = data[3]
        item.fields['version'] = data[4]
        item.fields['devtype'] = data[5]

        return item

class NmapOSItem(DBEntry):
    """Represent a single entry from the Nmap OS database."""

    def update(self, line):
        """Process a single line of the nmap OS database."""
        if line.startswith('Fingerprint'):
            line = line.replace('Fingerprint', '', 1)
            self.fields['title'] = line.strip().lower()
        elif line.startswith('Class'):
            line = line.replace('Class', '', 1)
            items = [x.strip().lower() for x in line.split('|')]
            self.fields['vendor'] = items[0]
            self.fields['product'] = items[1]
            self.fields['version'] = items[2]
            self.fields['devtype'] = items[3]

    def save(self, db):
        """Store a new item into the database."""
        t = (self.fields['title'],
             self.fields['vendor'],
             self.fields['product'],
             self.fields['version'],
             self.fields['devtype'])

        db.cursor.execute('INSERT INTO %s'
            ' (n_title,n_vendor,n_product,n_version,n_devtype)'
            ' VALUES (?,?,?,?,?)' % db.str_id, t)

    def __str__(self):
        """Return a human readable representation."""
        lines = ['%s => %s' % (k, v) for k, v in self.fields.iteritems()]
        return '\n'.join(lines) + '\n'

