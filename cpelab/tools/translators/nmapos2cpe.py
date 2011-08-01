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

"""Implementations of translation algorithms"""

from cpelab.tools.toolbase import SearchDB


class SimpleTranslator:
    """The most simple and naive translator. Compare fields and use translation
    tables to match entries.
    """
    str_id = 'simple'

    def __init__(self, pattern, db0, db1):
        """initialize a new simple translator"""
        raise NotImplementedError('Not implemented yet')

class FuzzyTranslator:
    """
    """
    str_id = 'fuzzy'

    def __init__(self, pattern, db0, db1):
        """attempt to map entries from db0 that match pattern to corresponding
        entries from db1.
        """
        print '[+] Attempting to convert entries matching: %s' % pattern

        src_sigs = SearchDB().lookup(db0, pattern)
        if len(src_sigs) == 0:
            print '[+] No match for "%s" in source db %s' % (pattern, db0.str_id)
            return

        print '[+] %d matches in source db %s' % (len(src_sigs), db0.str_id)
        for sig in src_sigs:
            print '-- %s --' % sig.fields['title']
            candidates = self._candidates(sig, db1)
            best_res = []
            best_score = -1
            for item in candidates:
                score = self._matching_score(sig, item)
                if score > best_score:
                    best_res = [item]
                    best_score = score
                elif score == best_score:
                    best_res.append(item)
            if len(best_res) > 0:
                #print 'score: %.02f' % best_score
                print '\n'.join([x.fields['name'] for x in best_res])

    def _candidates(self, ref_entry, db):
        """returned a reduced set, with the best candidates for matching"""

        categories = ['vendor', 'product', 'version']
        candidates = dict([(c, []) for c in categories])

        for item in db.entries:
            for cat in categories:
                if item.fields[cat] == ref_entry.fields[cat]:
                    candidates[cat].append(item)
                else:
                    break

        categories.reverse()
        for cat in categories:
            if len(candidates[cat]) > 0:
                return candidates[cat]

        # no match
        return []

    def _matching_score(self, ref, candidate):
        """return an arbitrary score (float) to express how similar are two
        entries
        """
        distance = self._levenshtein(ref.fields['title'], candidate.fields['title'])
        if distance == 0:
            return 2.
        else:
            return 1./distance

    def _levenshtein(self, str0, str1):
        """calculate and return the Levenshtein distance between two strings"""
        n, m = len(str0), len(str1)
        if n > m:
            str0, str1 = str1, str0
            n, m = m, n

        curr = range(n+1)
        for i in range(1, m+1):
            prev, curr = curr, [i] + [0]*n
            for j in range(1, n+1):
                add, delete = prev[j] + 1, curr[j-1] + 1
                change = prev[j-1]
                if str0[j-1] != str1[i-1]:
                    change = change + 1
                curr[j] = min(add, delete, change)
        return curr[n]

