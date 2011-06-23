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

from cpelab.auxiliary.auxmod import AuxModule, AuxModuleError


class VendorDiff(AuxModule):
    """this module performs a diff between vendors contained in two given
    databases. The result is displayed in a "diff-like" fashion. See the
    _display_results docstring for more information
    """
    str_id = 'vendor-diff'

    def __init__(self):
        """instanciate a new module"""
        AuxModule.__init__(self)
        self._diff_vendors = {}

    def start(self, targets):
        """module entry point. targets is a list of (two) db instances to
        compare
        """
        if len(targets) != 2:
            raise AuxModuleError('Invalid arguments')

        self._compute_diff(targets[0], targets[1])
        self._display_results()

    def _compute_diff(self, db0, db1):
        """Mark vendors as belonging to db0 only, db0 and db1 or db1 only"""
        for entry in db0.entries:
            self._diff_vendors[entry.vendor] = 0

        for entry in db1.entries:
            if not self._diff_vendors.has_key(entry.vendor):
                self._diff_vendors[entry.vendor] = 1
            elif self._diff_vendors[entry.vendor] == 0:
                # this entry exists in both dictionaries: delete it
                del self._diff_vendors[entry.vendor]

    def _display_results(self):
        """Display diff results in a diff-like fashion.

        - Vendors that are present in both db are ignored
        - Vendors that are only present in db0 are preceeded by '+'
        - Vendors that are only present in db1 are preceeded by '-'
        """
        for k, v in self._diff_vendors.iteritems():
            if v == 0:
                # only in db0
                print '+ %s' % k
            elif v == 1:
                # only in db1
                print '- %s' % k

    @classmethod
    def help_msg(cls, err=''):
        """return help message for this module"""
        return """%s
Module usage: labctl run %s <db0> <db1>
This module performs comparison between vendors listed in two given
databases.""" % (err, VendorDiff.str_id)

