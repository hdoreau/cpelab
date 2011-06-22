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

import xml.sax

from xml.sax.handler import ContentHandler

from cpelab.databases.db import Database, DBEntry


class CPEDict(Database):
    """CPE dictionnary"""
    
    remote = 'http://static.nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.2.xml'
    local = 'cpe_dict.xml'
    str_id = 'cpe-dict'

    def load(self):
        """load entries from the filesystem"""
        handler = CPEDictParser(self)
        xml.sax.parse(CPEDict.local_filename(), handler)
        self.loaded = True

class CPEDictParser(ContentHandler):
    """SAX content handler to load entries from the XML dictionary"""
    def __init__(self, cpedict):
        """
        """
        ContentHandler.__init__(self)
        self._cpe_dict = cpedict

        self._in_title = False
        self._name = ''
        self._title = ''

    def startElement(self, name, attrs):
        """callback: entering section"""
        if name == 'cpe-item' and not attrs.has_key('deprecated'):
            name = attrs['name']

            # Only deal with o and h entries
            # TODO fork this model to have two distinct database instances for
            # OS's and applications
            if not name.lower().startswith('cpe:/a:'):
                self._name = name
        elif name == 'title' and attrs['xml:lang'] == 'en-US':
            self._in_title = True

    def endElement(self, name):
        """callback: leaving section"""
        if name == 'title':
            self._in_title = False
        elif name == 'cpe-item':
            if len(self._title) > 0 and len(self._name) > 0:
                self._cpe_dict.entries.append(CPEItem(self._title, self._name))

            self._name = ''
            self._title = ''

    def characters(self, content):
        """callback: text to read"""
        if self._in_title:
            self._title += content

class CPEItem(DBEntry):
    """represent a single entry from the CPE dictionary"""
    def __init__(self, title, name):
        """instanciate a new entry"""
        DBEntry.__init__(self, title, name.split(':')[2])
        self.name = name

    def get_fields(self):
        """get the list of available values for this entry"""
        res = DBEntry.get_fields(self)
        res.append(self.name)
        return res

