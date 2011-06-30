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


"""Base classes for processing modules"""

import re

from cpelab.databases.utils import db_iter


class Tool:
    """abstract base class for processing modules."""
    str_id = None

    def __init__(self):
        """instanciate new processing module"""
        pass

    def start(self, args):
        """module entry point"""
        raise NotImplementedError('Abstract method subclasses must implement')

    @classmethod
    def help_msg(cls, err=''):
        """class method to return the syntaxic help message for this specific
        command
        """
        raise NotImplementedError('Abstract method subclasses must implement')

class UpdateDB(Tool):
    """download and install the latest version of the selected database(s)"""
    str_id = 'update'

    def start(self, args):
        """update existing DB (or create them)"""
        if len(args) != 1:
            raise RuntimeToolError('Invalid command line')

        for db_ref in db_iter(args[0]):
            db_ref.create_or_update()

    @classmethod
    def help_msg(cls, err=''):
        """return help message for the update command"""
        return """%s
Usage: labctl %s <db>
Download and extract the given database(s)""" % (err, cls.str_id)

class StatsDB(Tool):
    """count the number of entries and different vendors for the selected
    database(s)
    """
    str_id = 'stats'

    def start(self, args):
        """compute and display statistics about existing databases"""
        if len(args) != 1:
            raise RuntimeToolError('Invalid command line')

        for db_ref in db_iter(args[0]):
            db_ref.load()
            
            print '%s:' % db_ref.str_id
            print '\t%d entries loaded' % len(db_ref.entries)

            vendors = set()
            for cpe in db_ref.entries:
                vendors.add(cpe.fields['vendor'])

            print '\t%d vendors' % len(vendors)

    @classmethod
    def help_msg(cls, err=''):
        """return help message for the stats command"""
        return """%s
Usage: labctl %s <db>
Display statistics about the given database(s)""" % (err, cls.str_id)

class SearchDB(Tool):
    """load the selected database(s) and look for a given pattern in the
    entries
    """
    str_id = 'search'

    def start(self, args):
        """look for a given pattern in the selected database"""
        if len(args) != 2:
            raise RuntimeToolError('Invalid command line')

        pattern = args[0]
        db_spec = args[1]

        for db_ref in db_iter(db_spec):
            db_ref.load()
            res = self.lookup(db_ref, pattern)
            if len(res) == 0:
                print '%s: nothing found' % db_ref.str_id
            else:
                print '%s:' % db_ref.str_id
                for match in res:
                    print '%s' % str(match)

    def lookup(self, db, pattern):
        """look for a given pattern within the loaded entries"""
        res = []
        for entry in db.entries:
            if re.search(pattern, str(entry)) is not None:
                res.append(entry)
        return res

    @classmethod
    def help_msg(cls, err=''):
        """return help message for the search command"""
        return """%s
Usage: labctl %s <pattern> <db>
Look for a pattern in the given database(s)""" % (err, cls.str_id)

class RuntimeToolError(Exception):
    """base error for unexpected conditions while running tools"""

