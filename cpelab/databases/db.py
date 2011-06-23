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
import re
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
        self.load()

    def load(self):
        """load DB information from the filesystem"""
        raise NotImplementedError('Abstract method subclasses must implement')

    def display_info(self):
        """print statistics and factoids about the DB"""
        if not self.loaded:
            print '%s: not loaded' % self.__class__.str_id
            return

        print '%s:' % self.__class__.str_id
        print '\t%d entries loaded' % len(self.entries)

        fp_metacount = {}
        for cpe in self.entries:
            fp_metacount[cpe.vendor] = True

        print '\t%d vendors' % len(fp_metacount.keys())

    def lookup(self, pattern):
        """look for a given pattern within the loaded entries"""
        res = []
        for entry in self.entries:
            for element in entry.get_fields():
                if re.search(pattern, element) is not None:
                    res.append(entry)
                    break
        return res

    @classmethod
    def create_or_update(cls):
        """download latest version of the database from a remote location and
        store it locally
        """
        dest = cls.local_filename()

        print '[+] Updating %s...' % str(cls.str_id)
        resp = urllib2.urlopen(cls.remote)
        fout = open(dest, 'w')
        fout.write(resp.read())
        fout.close()
        print '[+] OK (see %s)' % dest

    @classmethod
    def local_filename(cls):
        """get local DB location"""
        return os.path.join(os.getcwd(), 'data', cls.local)

class DBEntry:
    """Represent a single database item"""
    def __init__(self, title, vendor):
        """instanciate a new item"""
        self.title = title
        self.vendor = vendor

    def get_fields(self):
        """return the values composing this item"""
        return [self.title, self.vendor]

