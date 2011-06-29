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
import urllib2


class Database:
    """Base (abstract) class for DB. Define a common interface for subclasses"""
    
    remote = None
    local = None
    str_id = None

    def __init__(self):
        """instanciate a new DB"""
        self.loaded = False
        self.entries = []

    def load(self):
        """load DB information from the filesystem if not done yet"""
        if not self.loaded:
            self._load_specific()
            self.loaded = True

    def create_or_update(self):
        """download latest version of the database from a remote location and
        store it locally
        """
        dest = self.local_filename()

        print '[+] Updating %s...' % str(self.str_id)
        resp = urllib2.urlopen(self.remote)

        fout = open(dest, 'w')
        print '[+] Shrinking base...'
        self._storage_filter(resp, fout)

        fout.close()
        print '[+] OK (see %s)' % dest

    def _load_specific(self):
        """actually load DB information"""
        raise NotImplementedError('Abstract method subclasses must implement')

    def _storage_filter(self, fin, fout):
        """
        """
        raise NotImplementedError('Abstract method subclasses must implement')

    @classmethod
    def local_filename(cls):
        """get local DB location"""
        return os.path.join(os.getcwd(), 'data', cls.local)

class DBEntry:
    """Represent a single database item"""
    def __init__(self):
        """instanciate a new item"""
        self.fields = {}

