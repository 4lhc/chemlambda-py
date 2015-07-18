
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  topology.py
#
#  author : Sreejith S
#  email  : echo $(base64 -d <<< NDQ0bGhjCg==)@gmail.com
#  date   : Sat 18 Jul 2015 17:53:16 IST
#  ver    : 

# Rules to read mol files 
#http://chorasimilarity.github.io/chemlambda-gui/dynamic/moves.html

#dict containg rules to identify ports for each atom
# mi = 'middle in', lo = 'left out' and so...
graph = { "L": [ "mi", "lo", "ro" ], 
        "FO": [ "mi", "lo", "ro" ],
        "FOE": [ "mi", "lo", "ro" ],
        "A": [ "li", "ri", "mo" ],
        "FI": [ "li", "ri", "mo" ],
        "Arrow": [ "mi", "mo" ],
        "T": [ "mi" ],
        "FRIN": [ "mo" ],
        "FROUT": [ "mi" ]
        }

