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


class Database:
    """Base (abstract) class for DB. Define a common interface for subclasses"""
    
    str_id = None

    def __init__(self):
        """instanciate a new DB"""
        self.loaded = False
        self.entries = []
        self.path = os.path.join(os.getcwd(), 'data', self.str_id)

    def load(self):
        """load DB information from the filesystem if not done yet"""
        if not self.loaded:
            self._load_specific()
            self.loaded = True

    def create_or_update(self):
        """Download and extract latest version of the database"""
        raise NotImplementedError('Abstract method subclasses must implement')

    def _load_specific(self):
        """Actually load information from the database into memory"""
        raise NotImplementedError('Abstract method subclasses must implement')

class DBEntry:
    """Represent a single database item"""
    def __init__(self):
        """instanciate a new item"""
        self.fields = {}

