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
from xml.sax.saxutils import XMLGenerator

from cpelab.databases.db import Database, DBEntry


class CPEDict(Database):
    """CPE dictionnary"""

    remote = 'http://static.nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.2.xml'
    local = 'cpe_dict.xml'
    str_id = 'cpe-dict'

    def _load_specific(self):
        """load entries from the filesystem"""
        handler = CPEDictParser(self)
        xml.sax.parse(CPEDict.local_filename(), handler)
        self.loaded = True

    def _storage_filter(self, fin, fout):
        """
        """
        generator = DictOSFilter(fout)
        xml.sax.parse(fin, generator)

class DictOSFilter(XMLGenerator):
    """produce a reduced CPE dict with only non-deprecated OS related entries"""
    def __init__(self, out):
        """instanciate a new filter"""
        XMLGenerator.__init__(self, out)
        self._reproduce = False
        self._discard_tag = ''

    def startElement(self, name, attrs):
        """callback: opening tag. Only keep OS related item, discard deprecated
        entries and non en-US titles.
        """
        if name == 'cpe-item' and not attrs.has_key('deprecated'):
            if not attrs['name'].startswith('cpe:/a'):
                self._reproduce = True
                attrs = {'name': attrs['name']} # discard all metadata

        if name == 'meta:item-metadata' or (name == 'title' and attrs['xml:lang'] != 'en-US'):
            self._discard_tag = name
            return

        if self._reproduce or name == 'cpe-list':
            XMLGenerator.startElement(self, name, attrs)

    def endElement(self, name):
        """callback: ending tag. Reproduce if this was a valid one"""
        if name == self._discard_tag:
            self._discard_tag = ''
            return

        if self._reproduce or name == 'cpe-list':
            XMLGenerator.endElement(self, name)

        if name == 'cpe-item':
            self._reproduce = False

    def characters(self, content):
        """callback: text. reproduce if this was contained within a valid tag"""
        if self._discard_tag == '' and self._reproduce:
            XMLGenerator.characters(self, content)

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
        DBEntry.__init__(self)

        self.fields['title'] = title
        self.fields['name'] = name

        name = name.replace('cpe:/', '')
        items = name.split(':')
        while len(items) < 7:
            items.append('')

        self.fields['part'] = items[0]
        self.fields['vendor'] = items[1]
        self.fields['product'] = items[2]
        self.fields['version'] = items[3]
        self.fields['udpate'] = items[4]
        self.fields['edition'] = items[5]
        self.fields['language'] = items[6]

    def __str__(self):
        """return a human readable representation"""
        return self.fields['name']

