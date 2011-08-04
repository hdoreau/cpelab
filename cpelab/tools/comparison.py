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


"""Processing modules to perform DB comparisons"""


from cpelab.tools.toolbase import Tool, RuntimeToolError
from cpelab.databases.utils import get_db


class BaseComparator(Tool):
    """Base abstract class to implement 2 db comparison tools"""

    def start(self, args):
        """Tool entry point. targets is a list of (two) db instances to
        compare.
        """
        if len(args) != 2:
            raise RuntimeToolError('Invalid arguments')

        db0 = get_db(args[0])
        db1 = get_db(args[1])

        if db0 is None:
            raise RuntimeToolError('Unknown database: %s' % args[0])
        if db1 is None:
            raise RuntimeToolError('Unknown database: %s' % args[1])

        db0.connect()
        db1.connect()

        self._compare(db0, db1)

        db0.close()
        db1.close()

    def _compare(self, db0, db1):
        """Comparison function. Compute and display results."""
        raise NotImplementedError('Abstract method subclasses must implement')

class VendorDiff(BaseComparator):
    """Diff vendors.
    
    This tool performs a diff between vendors contained in two given tables. The
    result is displayed in a "unified diff-like" fashion. See the _compare
    docstring for more information.
    """
    str_id = 'vendor-diff'

    def __init__(self):
        """Initialize a new VendorDiff instance."""
        BaseComparator.__init__(self)
        self._diff_vendors = {}

    def _compare(self, db0, db1):
        """Select vendors that are exclusively in db0 (displayed with a '+'
        prefix) or exclusively in db1 (displayed with a '-' prefix.
        """
        self._do_query(db0, db1)
        for vendor in db0.cursor.fetchall():
            print '+%s' % vendor[0]

        self._do_query(db1, db0)
        for vendor in db1.cursor.fetchall():
            print '-%s' % vendor[0]

    def _do_query(self, db0, db1):
        """Look for items that are exclusively present in db0."""
        db0.cursor.execute('select distinct %(db0)s.%(f0)s from %(db0)s where not exists (select id from %(db1)s where %(db1)s.%(f1)s = %(db0)s.%(f0)s)' \
            % {'db0': db0.str_id, 'db1': db1.str_id, 'f0': db0.dbfield('vendor'), 'f1': db1.dbfield('vendor')})

    @classmethod
    def help_msg(cls, err=''):
        """Return help message for the vendor-diff command."""
        return """%s
Usage: labctl %s <db0> <db1>
Compares vendor entries between two databases.""" % (err, VendorDiff.str_id)

class VendorCommon(BaseComparator):
    """This tool looks for common vendors between two databases."""
    str_id = 'vendor-common'

    def _compare(self, db0, db1):
        """Display vendors found in both databases."""
        # select distinct nmapos.n_vendor from nmapos where exists (select id from cpeos where cpe_vendor = nmapos.n_vendor)
        db0.cursor.execute('select distinct %(f0)s from %(db0)s where exists (select id from %(db1)s where %(f1)s = %(db0)s.%(f0)s)' \
            % {'db0': db0.str_id, 'db1': db1.str_id, 'f0':db0.dbfield('vendor'), 'f1':db1.dbfield('vendor')})

        for vendor in db0.cursor.fetchall():
            print vendor[0]

    @classmethod
    def help_msg(cls, err=''):
        """Return help message for the vendor-diff command."""
        return """%s
Usage: labctl %s <db0> <db1>
Display vendors found in both databases.""" % (err, VendorDiff.str_id)

