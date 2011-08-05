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

from cpelab.databases.db import Database
from cpelab.databases.utils import DBSpecParser, DBSpecError


class Tool:
    """Abstract base class for processing modules."""
    str_id = None

    def __init__(self):
        """Initialize a new Tool instance."""
        pass

    def start(self, args):
        """Module entry point."""
        raise NotImplementedError('Abstract method subclasses must implement')

    @classmethod
    def help_msg(cls, err=''):
        """Class method to return the syntaxic help message for this specific
        command.
        """
        raise NotImplementedError('Abstract method subclasses must implement')

class InitDB(Tool):
    """
    """
    str_id = 'init'

    def start(self, args):
        """Reset existing DB if exists and setup a new empty one."""
        print '[+] Initializing the whole database...'
        db = Database()
        db.initialize()
        print '[+] Done! You should now run "labctl update all" to populate the DB'

    @classmethod
    def help_msg(cls, err=''):
        """Return help message for the init command."""
        return """%s
Usage: labctl %s
Delete existing databases and recreate a new environment""" % (err, cls.str_id)

class UpdateDB(Tool):
    """Download and install the latest version of the selected database(s)."""
    str_id = 'update'

    def start(self, args):
        """Update databse from fresh upstream sources."""
        try:
            for db_ref in DBSpecParser(' '.join(args)):
                db_ref.populate()
        except DBSpecError, err:
            raise RuntimeToolError('Invalid arguments (%s)' % str(err))

    @classmethod
    def help_msg(cls, err=''):
        """Return help message for the update command."""
        return """%s
Usage: labctl %s <db>
Download and extract the given database(s)""" % (err, cls.str_id)

class StatsDB(Tool):
    """Count the number of entries and different vendors for the selected
    database(s).
    """
    str_id = 'stats'

    def start(self, args):
        """Compute and display statistics about existing databases."""
        try:
            for db_ref in DBSpecParser(' '.join(args)):
                print '%s:' % db_ref.str_id
                print '\t%d entries loaded' % db_ref.count()

                for field in ['vendor', 'product']:
                    print '\t%d %ss' % (db_ref.count(field), field)

        except DBSpecError, err:
            raise RuntimeToolError('Invalid arguments (%s)' % str(err))
            
    @classmethod
    def help_msg(cls, err=''):
        """Return help message for the stats command."""
        return """%s
Usage: labctl %s <db>
Display statistics about the given database(s)""" % (err, cls.str_id)

class SearchDB(Tool):
    """Search for a given pattern in the entries."""
    str_id = 'search'

    def start(self, args):
        """Look for a given pattern in the selected table(s)."""
        if len(args) != 2:
            raise RuntimeToolError('Invalid command line')

        pattern = args[0]

        try:
            for db_ref in DBSpecParser(args[1]):
                res = db_ref.lookup_all(pattern)
                if len(res) == 0:
                    print '%s: nothing found' % db_ref.str_id
                else:
                    print '[Matching items in %s]' % db_ref.str_id
                    for match in res:
                        print '%s' % str(match)
                    print "%d matching items in %s" % (len(res), db_ref.str_id)
        except DBSpecError, err:
            raise RuntimeToolError('Invalid arguments (%s)' % str(err))

    @classmethod
    def help_msg(cls, err=''):
        """Return help message for the search command."""
        return """%s
Usage: labctl %s <pattern> <db>
Look for a pattern in the given database(s)""" % (err, cls.str_id)

class RuntimeToolError(Exception):
    """Base error for unexpected conditions while running tools."""

