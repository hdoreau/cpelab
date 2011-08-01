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

import urllib2
import tempfile
import xml.sax

from xml.sax.handler import ContentHandler
from xml.sax.saxutils import XMLGenerator

from cpelab.databases.db import Database, DBEntry


CPE_DICT_LOCATION = 'http://static.nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.2.xml'

class CachedDict:
    """
    """
    is_cached = False
    fcached = tempfile.TemporaryFile()

    @classmethod
    def get(cls):
        """
        """
        if not cls.is_cached:
            print '[+] Caching CPE dictionary'
            resp = urllib2.urlopen(CPE_DICT_LOCATION)
            cls.fcached.write(resp.read())
            print '[+] OK'
            cls.is_cached = True

        cls.fcached.seek(0)
        return cls.fcached

class CPEOS(Database):
    """CPE dictionnary subset: operating systems and hardware"""

    str_id = 'cpe-os'

    def create_or_update(self):
        """
        """
        dest = self.path

        print '[+] Updating %s...' % str(CPEOS.str_id)
        full_db = CachedDict.get()

        fout = open(dest, 'w')
        print '[+] Shrinking base...'
        xml.sax.parse(full_db, CPEFilter(fout, 'oh'))

        fout.close()
        print '[+] OK (see %s)' % dest

    def _load_specific(self):
        """load entries from the filesystem"""
        xml.sax.parse(self.path, CPELoader(self))

class CPEApp(Database):
    """CPE dictionnary subset: applications"""

    str_id = 'cpe-app'

    def create_or_update(self):
        """
        """
        dest = self.path

        print '[+] Updating %s...' % str(CPEApp.str_id)
        full_db = CachedDict.get()

        fout = open(dest, 'w')
        print '[+] Shrinking base...'
        xml.sax.parse(full_db, CPEFilter(fout, 'a'))

        fout.close()
        print '[+] OK (see %s)' % dest

    def _load_specific(self):
        """load entries from the filesystem"""
        xml.sax.parse(self.path, CPELoader(self))

class CPEFilter(XMLGenerator):
    """produce a reduced CPE dict with only non-deprecated OS related entries"""
    def __init__(self, out, valid_parts):
        """instanciate a new filter"""
        XMLGenerator.__init__(self, out)
        self._reproduce = False
        self._discard_tag = ''
        self._valid_parts = valid_parts

    def startElement(self, name, attrs):
        """callback: opening tag. Only keep OS related item, discard deprecated
        entries and non en-US titles.
        """
        if name == 'cpe-item' and not attrs.has_key('deprecated'):
            # 5th char of a CPE name is the part (cpe:/a:...)
            if attrs['name'][5] in self._valid_parts:
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

class CPELoader(ContentHandler):
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
        if name == 'cpe-item':
            self._name = attrs['name']
        elif name == 'title':
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

        self.fields['title'] = title.lower()
        self.fields['name'] = name.lower()

        name = name[5::]
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
        lines = []
        for k in ['title', 'name']:
            lines.append('%s => %s' % (k.encode("utf-8"), self.fields[k].encode("utf-8")))
        return '\n'.join(lines) + '\n'

