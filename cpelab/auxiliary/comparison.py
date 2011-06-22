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


class AuxModule:
    """
    """

    str_id = None

    def start(self):
        """
        """
        raise NotImplementedError('Abstract method subclasses must implement')

    @classmethod
    def help_msg(cls):
        """
        """
        raise NotImplementedError('Abstract method subclasses must implement')

class VendorDiff(AuxModule):
    """
    """

    str_id = 'vendor-diff'

    def __init__(self):
        """
        """
        self._db0_vendors = {}
        self._db1_vendors = {}

    def start(self, targets):
        """
        """
        if len(targets) != 2:
            raise AuxModuleError('Invalid arguments')

        self._load_vendors(targets[0], targets[1])
        self._compute_diff()
        self._display_results()

    def _load_vendors(self, db0, db1):
        """
        """
        for entries in db0.entries:
            self._db0_vendors[entries.vendor] = 1

        for entries in db1.entries:
            self._db1_vendors[entries.vendor] = 1

    def _compute_diff(self):
        """
        """
        for vendor in self._db0_vendors.iterkeys():
            if self._db1_vendors.has_key(vendor):
                self._db0_vendors[vendor] = 0

        for vendor in self._db1_vendors.iterkeys():
            if not self._db0_vendors.has_key(vendor):
                self._db0_vendors[vendor] = -1

    def _display_results(self):
        """
        """
        for k, v in self._db0_vendors.iteritems():
            if v == -1:
                print '- %s' % k
            elif v == 1:
                print '+ %s' % k

    @classmethod
    def help_msg(cls, err=''):
        """
        """
        return """%s
Module usage: labctl run %s <db0> <db1>
This module performs comparison between vendors listed in two given
databases.""" % (err, VendorDiff.str_id)

class AuxModuleError(Exception):
    """base error for auxiliary module"""

