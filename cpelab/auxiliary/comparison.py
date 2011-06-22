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

import sys


class AuxModule:
    """
    """

    str_id = None

    def start(self):
        """
        """
        raise NotImplementedError('Abstract method subclasses must implement')

    @classmethod
    def display_help(cls):
        """
        """
        raise NotImplementedError('Abstract method subclasses must implement')

class VendorDiff(AuxModule):
    """
    """

    str_id = 'vendor-diff'

    def start(self, targets):
        """
        """
        if len(targets) != 2:
            VendorDiff.display_help('Invalid arguments')

    @classmethod
    def display_help(cls, err=''):
        """
        """
        sys.exit("""%s
Module usage: labctl run %s <db0> <db1>
This module performs comparison between vendors listed in two given
databases.""" % (err, VendorDiff.str_id))

