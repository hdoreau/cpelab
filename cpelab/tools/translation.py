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


"""Processing modules to perform DB translations"""

from cpelab.tools.toolbase import Tool, RuntimeToolError
from cpelab.databases.utils import get_db

from cpelab.databases.nmapos import NmapOS
from cpelab.databases.cpedict import CPEOS

from cpelab.tools.translators.nmapos2cpe import SimpleTranslator, FuzzyTranslator


class NmapOS2CPE(Tool):
    """this tool attempts to translate nmap os fingerprints into CPE"""
    str_id = 'nmapos2cpe'

    _translators = {
        SimpleTranslator.str_id: SimpleTranslator,
        FuzzyTranslator.str_id: FuzzyTranslator
    }
    _default_translator = SimpleTranslator.str_id

    def start(self, args):
        """tool entry point. targets is the list of arguments. It is expected to
        contains the title of the fingerprint to translate, the nmap-db to use
        and the cpe dictionary to use
        """
        if len(args) < 1:
            raise RuntimeToolError('Invalid arguments')

        pattern = args[0]

        nmap_db = NmapOS()
        cpe_db = CPEOS()

        nmap_db.load()
        cpe_db.load()

        if len(args) == 2:
            if self._translators.has_key(args[1]):
                translator = self._translators[args[1]]
            else:
                raise RuntimeToolError('Unknown translator: %s' % args[1])
        else:
            translator = self._translators[self._default_translator]

        translator(pattern, nmap_db, cpe_db)

    @classmethod
    def help_msg(cls, err=''):
        """return help message for the translate command"""
        return """%s
Usage: labctl %s <signature title> [translator]
Attempt to translate nmap signature into CPE.

Available translators are:
  %s
""" % (err, cls.str_id, '\n  '.join(cls._translators.keys()))
