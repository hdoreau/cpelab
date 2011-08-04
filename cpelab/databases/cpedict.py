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


"""CPE dictionary manipulation module"""

import urllib
import tempfile
import xml.sax

from xml.sax.handler import ContentHandler

from cpelab.databases.db import Database, DBEntry


CPE_DICT_LOCATION = 'http://static.nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.2.xml'


class CPEOS(Database):
    """CPE dictionary subset: operating systems and hardware."""
    str_id = 'cpeos'

    def __init__(self):
        """
        """
        Database.__init__(self)
        self.fields_map = {
            'title': 'cpe_title',
            'name': 'cpe_name',
            'part': 'cpe_part',
            'vendor': 'cpe_vendor',
            'product': 'cpe_product',
            'version': 'cpe_version',
            'update': 'cpe_update',
            'edition': 'cpe_edition',
            'language': 'cpe_language'
        }
        self._search_fields = ['title', 'name']

    def populate(self):
        """Load items into the corresponding table of the database."""
        print '[+] Updating %s...' % str(CPEOS.str_id)

        self.connect()
        full_db, _ = urllib.urlretrieve(CPE_DICT_LOCATION)

        print '[+] Storing base...'

        xml.sax.parse(full_db, CPEFilter(self, 'oh'))

        self.close()

        # XXX display statistics
        print '[+] Update complete!'

    def _make_item(self, data):
        """Make and return an item (object) from selected fields from the database."""
        item = CPEItem()
        # data[0] is the DB id, discard it
        item.update({'title': data[1], 'name': data[2]})
        return item

class CPEFilter(ContentHandler):
    """Produce a reduced CPE dict with only non-deprecated OS related entries
    and store the valid entries into the database."""
    def __init__(self, db, valid_parts):
        """Initialize a new CPEFilter instance."""
        ContentHandler.__init__(self)
        self.db = db
        self._tmp_item = None
        self._valid_parts = valid_parts

        # internal parsing flag
        self._in_title = False
        self._discard = False

        self._curr_title = []

    def startElement(self, name, attrs):
        """Callback: opening XML tag. Only keep OS related item, discard
        deprecated entries and non en-US titles.
        """
        if self._discard:
            return

        if name == 'cpe-item':
            if attrs.has_key('deprecated'):
                self._discard = True
            else:
                # 5th char of a CPE name is the part (cpe:/a:...)
                if attrs['name'][5] in self._valid_parts:
                    self._tmp_item = CPEItem()
                    self._tmp_item.update({'name': attrs['name']})
                else:
                    self._discard = True
        elif (not self._discard) and (name == 'title') and (attrs['xml:lang'] == 'en-US'):
            self._curr_title = []
            self._in_title = True

    def endElement(self, name):
        """Callback: ending XML tag"""
        if name == 'cpe-item':
            if self._tmp_item is not None:
                self._tmp_item.save(self.db)
            self._tmp_item = None
            self._discard = False
        elif name == 'title':
            if self._in_title:
                self._tmp_item.update({'title': ''.join(self._curr_title)})
                self._curr_title = []
                self._in_title = False

    def characters(self, content):
        """Callback: text."""
        if self._in_title:
            self._curr_title.append(content)

class CPEItem(DBEntry):
    """Represent a single entry from the CPE dictionary."""
    def update(self, components):
        """Update an existing instance."""
        if components.has_key('title'):
            self.fields['title'] = components['title'].lower()
        if components.has_key('name'):
            name = components['name'].lower()
            self.fields['name'] = name

            name = name[5::]
            items = name.split(':')
            while len(items) < 7:
                items.append('')

            self.fields['part'] = items[0]
            self.fields['vendor'] = items[1]
            self.fields['product'] = items[2]
            self.fields['version'] = items[3]
            self.fields['update'] = items[4]
            self.fields['edition'] = items[5]
            self.fields['language'] = items[6]

    def save(self, db):
        """Store a new item into the database."""
        fields = ['title', 'name', 'part', 'vendor', 'product', 'version',
            'update', 'edition', 'language']

        t = tuple([self.fields[x] for x in fields])
        fdesc = ','.join(['cpe_' + x for x in fields])

        db.cursor.execute('INSERT INTO %s (%s) VALUES (?,?,?,?,?,?,?,?,?)' % (db.str_id, fdesc), t)

    def __str__(self):
        """Return a human readable representation."""
        lines = []
        for k in ['title', 'name']:
            lines.append('%s => %s' % (k.encode("utf-8"), self.fields[k].encode("utf-8")))
        return '\n'.join(lines) + '\n'

