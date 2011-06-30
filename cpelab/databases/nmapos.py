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
    """Nmap OS fingerprints database"""

    str_id = 'nmap-os'

    def __init__(self):
        """instanciate a new Nmap OS DB"""
        Database.__init__(self)
        self._item_title = None

    def create_or_update(self):
        """download latest version of the database from a remote location and
        store it locally
        """
        dest = self.path

        print '[+] Updating %s...' % str(NmapOS.str_id)
        resp = urllib2.urlopen(NMAP_OS_DICT_LOCATION)

        fout = open(dest, 'w')
        print '[+] Shrinking base...'
        for line in resp:
            if line.startswith('Fingerprint') or line.startswith('Class'):
                fout.write(line)
        fout.close()
        print '[+] OK (see %s)' % dest

    def _load_specific(self):
        """load entries from local file"""
        fin = open(self.path)
        try:
            for line in fin:
                self._process_line(line)
        finally:
            fin.close()

    def _process_line(self, line):
        """process a single line of the nmap OS database"""
        if line.startswith('Fingerprint'):
            self._item_title = line.replace('Fingerprint', '', 1)
            self._item_title = self._item_title.strip()

        elif line.startswith('Class'):
            fp_meta = line.replace('Class', '', 1)
            fp_meta = [x.strip() for x in fp_meta.split('|')]
            fp_meta.insert(0, self._item_title)
            os_entry = NmapOSItem(fp_meta)

            self.entries.append(os_entry)

class NmapOSItem(DBEntry):
    """represent a single entry from the Nmap OS database"""
    def __init__(self, items):
        """instanciate a new entry"""
        DBEntry.__init__(self)
        self.fields['title'] = items[0].lower()
        self.fields['vendor'] = items[1].lower()
        self.fields['product'] = items[2].lower()
        self.fields['version'] = items[3].lower()
        self.fields['devtype'] = items[4].lower()

    def __str__(self):
        """return a human readable representation"""
        lines = ['%s => %s' % (k, v) for k, v in self.fields.iteritems()]
        return '\n'.join(lines) + '\n'
