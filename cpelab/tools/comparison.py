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
        """tool entry point. targets is a list of (two) db instances to
        compare
        """
        if len(args) != 2:
            raise RuntimeToolError('Invalid arguments')

        db0 = get_db(args[0])
        db1 = get_db(args[1])

        if db0 is None:
            raise RuntimeToolError('Unknown database: %s' % args[0])
        if db1 is None:
            raise RuntimeToolError('Unknown database: %s' % args[1])

        print 'Loading databases...'
        db0 = db0()
        db1 = db1()
        self._compare(db0, db1)

    def _compare(self, db0, db1):
        """comparison function. Compute and display resutls"""
        raise NotImplementedError('Abstract method subclasses must implement')


class VendorDiff(BaseComparator):
    """this tool performs a diff between vendors contained in two given
    databases. The result is displayed in a "diff-like" fashion. See the
    _compute_diff docstring for more information
    """
    str_id = 'vendor-diff'

    def __init__(self):
        """instanciate a new VendorDiff tool"""
        BaseComparator.__init__(self)
        self._diff_vendors = {}

    def _compare(self, db0, db1):
        """Select vendors that are exclusively in db0 (displayed with a '+'
        prefix) or exclusively in db1 (displayed with a '-' prefix.
        """
        vendors0 = set([entry.vendor for entry in db0.entries])
        vendors1 = set([entry.vendor for entry in db1.entries])

        res = vendors0 - vendors1
        for vendor in res:
            print '+ %s' % vendor
        
        res = vendors1 - vendors0
        for vendor in res:
            print '- %s' % vendor

    @classmethod
    def help_msg(cls, err=''):
        """return help message for the vendor-diff command"""
        return """%s
Usage: labctl %s <db0> <db1>
Compares vendor entries between two databases.""" % (err, VendorDiff.str_id)

class VendorCommon(BaseComparator):
    """this tool looks for common vendors between two databases"""
    str_id = 'vendor-common'

    def _compare(self, db0, db1):
        """display vendors found in both databases"""
        vendors0 = set([entry.vendor for entry in db0.entries])
        vendors1 = set([entry.vendor for entry in db1.entries])

        res = vendors0 & vendors1
        for vendor in res:
            print vendor

    @classmethod
    def help_msg(cls, err=''):
        """return help message for the vendor-diff command"""
        return """%s
Usage: labctl %s <db0> <db1>
Display vendors found in both databases.""" % (err, VendorDiff.str_id)

