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


"""Base classes for auxiliary processing modules"""


class AuxModule:
    """abstract class for auxiliary modules."""
    str_id = None

    def start(self):
        """module entry point"""
        raise NotImplementedError('Abstract method subclasses must implement')

    @classmethod
    def help_msg(cls):
        """class method to return the syntaxic help message for this specific
        module
        """
        raise NotImplementedError('Abstract method subclasses must implement')

class AuxModuleError(Exception):
    """base error for auxiliary module"""

