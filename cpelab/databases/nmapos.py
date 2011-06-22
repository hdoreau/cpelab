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

from cpelab.databases.db import Database, DBEntry


class NmapOS(Database):
    """Nmap OS fingerprints database"""
    
    remote = 'http://nmap.org/svn/nmap-os-db'
    local = 'nmap-os-db'
    str_id = 'nmap-os'

    def __init__(self):
        """instanciate a new Nmap OS DB"""
        Database.__init__(self)
        self._item_title = None

    def load(self):
        """load entries from local file"""
        fin = open(NmapOS.local_filename())
        try:
            for line in fin:
                self._process_line(line)
        finally:
            fin.close()

        self.loaded = True

    def _process_line(self, line):
        """process a single line of the nmap OS database"""
        if line.startswith('Fingerprint'):
            self._item_title = line.replace('Fingerprint', '', 1)
            self._item_title = self._item_title.strip()

        elif line.startswith('Class'):
            fp_meta = line.replace('Class', '', 1)
            fp_meta = [x.strip().lower() for x in fp_meta.split('|')]
            fp_meta.insert(0, self._item_title.lower())
            os = NmapOSItem(*fp_meta)

            self.entries.append(os)

class NmapOSItem(DBEntry):
    """represent a single entry from the Nmap OS database"""
    def __init__(self, title, vendor, family, gen, devtype):
        """instanciate a new entry"""
        DBEntry.__init__(self, title, vendor)
        self.family = family
        self.generation = gen
        self.device_type = devtype

    def get_fields(self):
        """get the list of available values for this entry"""
        res = DBEntry.get_fields(self)
        res.append(self.family)
        res.append(self.generation)
        res.append(self.device_type)
        return res

    def __str__(self):
        """
        """
        return '%s %s %s %s %s' % (self.title, self.vendor, self.family, \
            self.generation, self.device_type)

