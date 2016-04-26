#!/usr/bin/env python
"""
This code is part of the Mathematical Programming Toolbox PyMPL.

Copyright (C) 2015-2016, Filipe Brandao
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function
from builtins import range
from builtins import map


def read_table(fname, index1, index2, transpose=False):
    """Reads a table from a file."""
    if transpose:
        index1, index2 = index2, index1
    with open(fname) as f:
        text = f.read().replace(",", "")
        lst = list(map(float, text.split()))
        demand = {}
        for i1 in index1:
            for i2 in index2:
                if transpose:
                    demand[i2, i1] = lst.pop(0)
                else:
                    demand[i1, i2] = lst.pop(0)
        assert lst == []
        return demand


def main():
    """Parses 'ppbymip_cgp.mod'"""
    from pympl import PyMPL, Tools, glpkutils

    mod_in = "ppbymip_cgp.mod"
    mod_out = "tmp/cgp.out.mod"
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/cgp.lp"
    glpkutils.mod2lp(mod_out, lp_out, True)
    try:
        out, varvalues = Tools.script(
            "gurobi_wrapper.sh", lp_out,
            options="Threads=1 Presolve=0 Heuristics=0.25 MIPGap=0",
            verbose=True
        )
    except RuntimeError as e:
        print(repr(e))

    # print("varvalues:", [(k, v) for k, v in sorted(varvalues.items())])


if __name__ == "__main__":
    import os
    sdir = os.path.dirname(__file__)
    if sdir != "":
        os.chdir(sdir)
    main()
