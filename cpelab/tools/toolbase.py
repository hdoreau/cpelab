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

from cpelab.databases.utils import db_iter


class Tool:
    """abstract base class for processing modules."""
    str_id = None

    def __init__(self):
        """instanciate new processing module"""
        pass

    def start(self):
        """module entry point"""
        raise NotImplementedError('Abstract method subclasses must implement')

    @classmethod
    def help_msg(cls, err=''):
        """class method to return the syntaxic help message for this specific
        command
        """
        raise NotImplementedError('Abstract method subclasses must implement')

class UpdateDB(Tool):
    """
    """
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
Download and extract the given database(s)""" % (err, UpdateDB.str_id)

class StatsDB(Tool):
    """
    """
    str_id = 'stats'

    def start(self, args):
        """compute and display statistics about existing databases"""
        if len(args) != 1:
            raise RuntimeToolError('Invalid command line')

        for db_ref in db_iter(args[0]):
            db_ref().display_info()

    @classmethod
    def help_msg(cls, err=''):
        """return help message for the stats command"""
        return """%s
Usage: labctl %s <db>
Display statistics about the given database(s)""" % (err, StatsDB.str_id)

class SearchDB(Tool):
    """
    """
    str_id = 'search'

    def start(self, args):
        """look for a given pattern in the selected database"""
        if len(args) != 1:
            raise RuntimeToolError('Invalid command line')

        for db_ref in db_iter(args[0]):
            res = db_ref().lookup(item)
            if len(res) == 0:
                print '%s: nothing found' % db_ref.str_id
            else:
                print '%s:' % db_ref.str_id
                for match in res:
                    print '%s' % str(match)

    @classmethod
    def help_msg(cls, err=''):
        """return help message for the search command"""
        return """%s
Usage: labctl %s <pattern> <db>
Look for a pattern in the given database(s)""" % (err, SearchDB.str_id)

class RuntimeToolError(Exception):
    """base error for unexpected conditions while running tools"""

